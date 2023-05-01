from flask import Flask, Response
import subprocess

app = Flask(__name__)


@app.route('/hls')
def hls_playlist():
    playlist_file = 'output/playlist.m3u8'
    # Start ffmpeg to convert video stream to HLS
    ffmpeg_cmd = ['ffmpeg', '-i', 'http://192.168.137.247:4747/video', '-codec', 'copy', '-start_number', '0',
                  '-hls_time', '10', '-hls_list_size', '6', '-f', 'hls', 'output/playlist.m3u8']
    subprocess.Popen(ffmpeg_cmd)

    with open(playlist_file, 'r') as f:
        playlist = f.read()
        print(playlist)
    return Response(playlist, mimetype='application/vnd.apple.mpegurl')


@app.route('/hls/<path:path>')
def hls_segments(path):
    segment_file = f'output/{path}'
    with open(segment_file, 'rb') as f:
        segment = f.read()
    return Response(segment, mimetype='video/MP2T')


if __name__ == '__main__':
    # Start Flask server
    app.run(host='0.0.0.0', port=8080)
