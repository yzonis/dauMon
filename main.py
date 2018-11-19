import subprocess as sp
import os
import numpy as np
import matplotlib.pyplot as plt

###############
# User settings
###############

ffmpegPath = '../ffmpeg/bin/ffmpeg.exe'
outPath    = './tmp.mp4'

############
# Structures
############

ffmpegPath = os.path.realpath(ffmpegPath)
outPath    = os.path.realpath(outPath)

fig   = plt.figure()
ax    = plt.axes()
line, = ax.plot(np.random.rand(321,))
ax.set_ylim([-1,1])
ax.set_title('a simple figure')
fig.canvas.draw()
d     = fig.canvas.get_width_height()

########
# Action
########

command = [ ffmpegPath,
            '-y', # (optional) overwrite output file if it exists
            '-f', 'rawvideo',
            '-vcodec','rawvideo',
            '-s', str(d[0])+'x'+str(d[1]), # size of one frame
            '-pix_fmt', 'rgb24',
            '-r', '24', # frames per second
            '-i', '-', # The input comes from a pipe
            '-an', # Tells FFMPEG not to expect any audio
            '-vcodec', 'mpeg4',
            '-b:v','5M', # target bit-rate
            outPath ]

pipe = sp.Popen(command,shell=True,stdin=sp.PIPE,stderr=sp.PIPE)

for i in range(24*5):
    line.set_ydata(np.random.rand(321,))
    fig.canvas.draw()
    pipe.stdin.write(fig.canvas.tostring_rgb())
