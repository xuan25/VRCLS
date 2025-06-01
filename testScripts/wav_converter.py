import os
import sys
import argparse
from pydub import AudioSegment
from pydub.utils import mediainfo
import time
def set_ffmpeg_paths(ffmpeg_path=None, ffprobe_path=None):
    """
    Optionally sets the path to ffmpeg and ffprobe for Pydub.
    """
    if ffmpeg_path:
        if not os.path.isfile(ffmpeg_path):
            print(f"Warning: Specified ffmpeg path not found: {ffmpeg_path}")
            # Or raise FileNotFoundError(f"ffmpeg not found at: {ffmpeg_path}")
        else:
            AudioSegment.converter = ffmpeg_path
            print(f"Using custom ffmpeg: {AudioSegment.converter}")

    if ffprobe_path:
        if not os.path.isfile(ffprobe_path):
            print(f"Warning: Specified ffprobe path not found: {ffprobe_path}")
            # Or raise FileNotFoundError(f"ffprobe not found at: {ffprobe_path}")
        else:
            # Pydub uses its own logic for ffprobe if AudioSegment.ffprobe is not set
            # Forcing it can sometimes be useful, or relying on pydub's discovery
            # If you specifically want to override pydub's ffprobe discovery:
            # from pydub.utils import get_ffprobe_internals
            # get_ffprobe_internals.FFPROBE_PATH = ffprobe_path
            # Or, more directly if available in your pydub version:
            if hasattr(AudioSegment, 'ffprobe') and AudioSegment.ffprobe is not None: # Check if settable
                 AudioSegment.ffprobe = ffprobe_path
            else: # Fallback to modify where mediainfo looks
                 mediainfo.FFPROBE_PATH = ffprobe_path
            print(f"Using custom ffprobe (via mediainfo or AudioSegment): {ffprobe_path}")
    
    # Verify Pydub can find them (optional, pydub does this on first use)
    try:
        # This will trigger ffprobe discovery if not explicitly set
        AudioSegment.from_file(os.devnull, format="wav") # Dummy load to test setup
    except Exception as e:
        if "ffmpeg" in str(e).lower() or "ffprobe" in str(e).lower():
            print(f"Warning: Pydub might not find ffmpeg/ffprobe. Conversion might fail: {e}")
            print("Ensure ffmpeg and ffprobe are in your PATH, next to this script/executable, or specified via --ffmpeg/--ffprobe.")


def convert_wav(input_path, output_dir="output", formats_to_convert=["ogg", "aac"]):
    """
    Converts a single WAV file to specified formats.
    """
    if not os.path.isfile(input_path):
        print(f"Error: Input file not found: {input_path}")
        return

    if not input_path.lower().endswith(".wav"):
        print(f"Skipping non-WAV file: {input_path}")
        return

    print(f"Processing: {input_path}")
    os.makedirs(output_dir, exist_ok=True)

    try:
        audio = AudioSegment.from_wav(input_path)
    except Exception as e:
        print(f"Error loading WAV file {input_path}: {e}")
        return

    base_filename = os.path.splitext(os.path.basename(input_path))[0]

    for fmt in formats_to_convert:
        fmt = fmt.lower().strip()
        output_filename = os.path.join(output_dir, f"{base_filename}.{fmt}")
        
        try:
            t1=time.time()
            print(f"  Converting to {fmt.upper()} -> {output_filename}")
            if fmt == "aac":
                # AAC is often stored in an M4A container. Pydub handles this.
                # You might need to specify bitrate for quality.
                audio.export(output_filename, format="adts", bitrate="192k") # Raw AAC stream
                # Or for M4A container:
                # audio.export(output_filename, format="mp4", codec="aac", bitrate="192k") 
                # pydub default for format="aac" is usually good for .aac extension
                # audio.export(output_filename, format="aac", bitrate="192k")
            elif fmt == "ogg":
                # OGG Vorbis
                audio.export(output_filename, format="ogg", codec="libvorbis", bitrate="192k")
            else:
                print(f"  Unsupported format: {fmt}. Skipping.")
                continue
            t2=time.time()
            print(f"  Successfully converted to {output_filename}.time:{t2-t1}s")
        except Exception as e:
            print(f"  Error converting {input_path} to {fmt.upper()}: {e}")
            print(f"  Make sure FFmpeg is installed and accessible (PATH or specified).")

def main():
    parser = argparse.ArgumentParser(description="Convert WAV files to OGG and/or AAC format using Pydub.")
    parser.add_argument("--input_path",default='1748420981.4904928-file.wav', help="Path to the input WAV file or directory containing WAV files.")
    parser.add_argument("-o", "--output_dir", default="output", help="Directory to save converted files. Default is 'output'.")
    parser.add_argument("--formats", default="aac,ogg", help="Comma-separated list of target formats (e.g., 'ogg,aac'). Default is 'ogg,aac'.")
    parser.add_argument("--ffmpeg_path", help="Optional: Full path to the ffmpeg executable.")
    parser.add_argument("--ffprobe_path", help="Optional: Full path to the ffprobe executable.")
    
    args = parser.parse_args()
    # Set FFmpeg/FFprobe paths if provided
    set_ffmpeg_paths('ffmpeg/bin/ffmpeg.exe', 'ffmpeg/bin/ffprobe.exe')

    target_formats = [fmt.strip().lower() for fmt in args.formats.split(',')]
    if not target_formats or all(not f for f in target_formats):
        print("Error: No valid target formats specified.")
        sys.exit(1)

    if os.path.isfile(args.input_path):
        convert_wav(args.input_path, args.output_dir, target_formats)
    elif os.path.isdir(args.input_path):
        print(f"Processing WAV files in directory: {args.input_path}")
        found_wav = False
        for item in os.listdir(args.input_path):
            if item.lower().endswith(".wav"):
                found_wav = True
                full_path = os.path.join(args.input_path, item)
                convert_wav(full_path, args.output_dir, target_formats)
        if not found_wav:
            print(f"No WAV files found in directory: {args.input_path}")
    else:
        print(f"Error: Input path '{args.input_path}' is not a valid file or directory.")
        sys.exit(1)

    print("Conversion process finished.")

if __name__ == "__main__":
    main()