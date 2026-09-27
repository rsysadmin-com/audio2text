import argparse
import sys

from datetime import datetime
from importlib.metadata import version
from pathlib import Path

from faster_whisper import WhisperModel

def parse_args():
    parser = argparse.ArgumentParser(
        prog="audio2text",
        description="Transcribe audio files locally using faster-whisper.",
    )

    parser.add_argument(
        "-V",
        "--version",
        action="version",
        version=f"%(prog)s {version('audio2text')}",
    )
        
    parser.add_argument(
        "files",
        nargs="+",
        type=Path,
        help="Audio file(s) to transcribe",
    )

    parser.add_argument(
        "-l",
        "--language",
        default="auto",
        help="Language code (pt, es, en, de, etc.) or 'auto' (default: auto)",
    )

    parser.add_argument(
        "-m",
        "--model",
        default="large-v3",
        help="Whisper model to use (default: large-v3)",
    )

    parser.add_argument(
        "-d",
        "--device",
        choices=["cpu", "cuda", "auto"],
        default="cpu",
        help="Device used for inference (default: cpu)",
    )

    parser.add_argument(
        "--compute-type",
        default=None,
        help="CTranslate2 compute type, e.g. int8, float16, float32",
    )

    parser.add_argument(
        "-t",
        "--timestamps",
        action="store_true",
        help="Include timestamps in the transcript",
    )

    parser.add_argument(
        "-o",
        "--output",
        action="store_true",
        help="Save transcript to transcript_YYYYMMDD_HHMMSS.txt",
    )

    return parser.parse_args()


def format_timestamp(seconds):
    milliseconds = int(round(seconds * 1000))

    hours, milliseconds = divmod(milliseconds, 3_600_000)
    minutes, milliseconds = divmod(milliseconds, 60_000)
    secs, milliseconds = divmod(milliseconds, 1000)

    return f"{hours:02d}:{minutes:02d}:{secs:02d}.{milliseconds:03d}"


def build_model(args):
    kwargs = {
        "device": args.device,
    }

    if args.compute_type:
        kwargs["compute_type"] = args.compute_type
    elif args.device == "cpu":
        kwargs["compute_type"] = "int8"

    print(
        f"Loading model '{args.model}' on {args.device}...",
        file=sys.stderr,
    )

    return WhisperModel(args.model, **kwargs)


def transcribe_file(model, path, language, timestamps):
    segments, info = model.transcribe(
        str(path),
        language=language,
        vad_filter=True,
    )

    # faster-whisper returns a generator.
    # Converting it to a list performs the actual transcription.
    segments = list(segments)

    lines = []

    lines.append(f"===== {path.name} =====")

    if language is None:
        probability = info.language_probability * 100
        lines.append(
            f"[Language: {info.language} ({probability:.1f}%)]"
        )

    if timestamps:
        for segment in segments:
            text = segment.text.strip()

            if not text:
                continue

            start = format_timestamp(segment.start)
            end = format_timestamp(segment.end)

            lines.append(
                f"[{start} --> {end}] {text}"
            )
    else:
        text = "".join(
            segment.text for segment in segments
        ).strip()

        if text:
            lines.append(text)

    return "\n".join(lines)


def main():
    args = parse_args()

    language = (
        None
        if args.language.lower() == "auto"
        else args.language.lower()
    )

    valid_files = []

    for path in args.files:
        if not path.is_file():
            print(
                f"Error: file not found: {path}",
                file=sys.stderr,
            )
        else:
            valid_files.append(path)

    if not valid_files:
        print(
            "Error: no valid input files.",
            file=sys.stderr,
        )
        sys.exit(1)

    try:
        model = build_model(args)
    except Exception as exc:
        print(
            f"Error loading model: {exc}",
            file=sys.stderr,
        )
        sys.exit(1)

    transcripts = []

    for path in valid_files:
        try:
            transcript = transcribe_file(
                model=model,
                path=path,
                language=language,
                timestamps=args.timestamps,
            )

            transcripts.append(transcript)

            print()
            print(transcript)

        except Exception as exc:
            print(
                f"\nError transcribing '{path}': {exc}",
                file=sys.stderr,
            )

    if args.output and transcripts:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = Path.cwd() / f"transcript_{timestamp}.txt"

        output_text = "\n\n".join(transcripts) + "\n"

        output_file.write_text(
            output_text,
            encoding="utf-8",
        )

        print(
            f"\nTranscript saved to: {output_file}",
            file=sys.stderr,
        )


if __name__ == "__main__":
    main()
