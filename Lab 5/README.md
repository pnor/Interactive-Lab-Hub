# Observant Systems

**Philip Parvaneh, Phillip O’Reggio, Lineker Ono-Lozano**


For lab this week, we focus on creating interactive systems that can detect and respond to events or stimuli in the environment of the Pi, like the Boat Detector we mentioned in lecture. 
Your **observant device** could, for example, count items, find objects, recognize an event or continuously monitor a room.

This lab will help you think through the design of observant systems, particularly corner cases that the algorithms need to be aware of.

## Prep

1. Spend about 10 Minutes doing the Listening exercise as described in [ListeningExercise.md](https://github.com/FAR-Lab/Interactive-Lab-Hub/blob/Fall2022/Lab%205/ListeningExercise.md)
2.  Install VNC on your laptop if you have not yet done so. This lab will actually require you to run script on your Pi through VNC so that you can see the video stream. Please refer to the [prep for Lab 2](https://github.com/FAR-Lab/Interactive-Lab-Hub/blob/Fall2022/Lab%202/prep.md), we offered the instruction at the bottom.
3.  Read about [OpenCV](https://opencv.org/about/), [MediaPipe](https://mediapipe.dev/), and [TeachableMachines](https://teachablemachine.withgoogle.com/).
4.  Read Belloti, et al.'s [Making Sense of Sensing Systems: Five Questions for Designers and Researchers](https://www.cc.gatech.edu/~keith/pubs/chi2002-sensing.pdf).

### For the lab, you will need:
1. Pull the new Github Repo.(Please wait until Thursday morning. There are still some incompatibilities to make the assignment work.)
1. Raspberry Pi
1. Webcam 

### Deliverables for this lab are:
1. Show pictures, videos of the "sense-making" algorithms you tried.
1. Show the filled out answers for the Contextual Interaction Design Tool.
1. Show a video of how you embed one of these algorithms into your observant system.
1. Test, characterize your interactive device. Show faults in the detection and how the system handled it.

## Overview
Building upon the paper-airplane metaphor (we're understanding the material of machine learning for design), here are the four sections of the lab activity:

A) [Play](#part-a)

B) [Fold](#part-b)

C) [Flight test](#part-c)

D) [Reflect](#part-d)

---

### Part A
### Play with different sense-making algorithms.

#### OpenCV
A more traditional method to extract information out of images is provided with OpenCV. The RPI image provided to you comes with an optimized installation that can be accessed through python. We included 4 standard OpenCV examples: contour(blob) detection, face detection with the ``Haarcascade``, flow detection (a type of keypoint tracking), and standard object detection with the [Yolo](https://pjreddie.com/darknet/yolo/) darknet.

Most examples can be run with a screen (e.g. VNC or ssh -X or with an HDMI monitor), or with just the terminal. The examples are separated out into different folders. Each folder contains a ```HowToUse.md``` file, which explains how to run the python example. 

The following command is a nicer way you can run and see the flow of the `openCV-examples` we have included in your Pi. Instead of `ls`, the command we will be using here is `tree`. [Tree](http://mama.indstate.edu/users/ice/tree/) is a recursive directory colored listing command that produces a depth indented listing of files. Install `tree` first and `cd` to the `openCV-examples` folder and run the command:

```shell
pi@ixe00:~ $ sudo apt install tree
...
pi@ixe00:~ $ cd openCV-examples
pi@ixe00:~/openCV-examples $ tree -l
.
├── contours-detection
│   ├── contours.py
│   └── HowToUse.md
├── data
│   ├── slow_traffic_small.mp4
│   └── test.jpg
├── face-detection
│   ├── face-detection.py
│   ├── faces_detected.jpg
│   ├── haarcascade_eye_tree_eyeglasses.xml
│   ├── haarcascade_eye.xml
│   ├── haarcascade_frontalface_alt.xml
│   ├── haarcascade_frontalface_default.xml
│   └── HowToUse.md
├── flow-detection
│   ├── flow.png
│   ├── HowToUse.md
│   └── optical_flow.py
└── object-detection
    ├── detected_out.jpg
    ├── detect.py
    ├── frozen_inference_graph.pb
    ├── HowToUse.md
    └── ssd_mobilenet_v2_coco_2018_03_29.pbtxt
```

The flow detection might seem random, but consider [this recent research](https://cseweb.ucsd.edu/~lriek/papers/taylor-icra-2021.pdf) that uses optical flow to determine busy-ness in hospital settings to facilitate robot navigation. Note the velocity parameter on page 3 and the mentions of optical flow.

Now, connect your webcam to your Pi and use **VNC to access to your Pi** and open the terminal. Use the following command lines to try each of the examples we provided:
(***it will not work if you use ssh from your laptop***)

```
pi@ixe00:~$ cd ~/openCV-examples/contours-detection
pi@ixe00:~/openCV-examples/contours-detection $ python contours.py
...
pi@ixe00:~$ cd ~/openCV-examples/face-detection
pi@ixe00:~/openCV-examples/face-detection $ python face-detection.py
...
pi@ixe00:~$ cd ~/openCV-examples/flow-detection
pi@ixe00:~/openCV-examples/flow-detection $ python optical_flow.py 0 window
...
pi@ixe00:~$ cd ~/openCV-examples/object-detection
pi@ixe00:~/openCV-examples/object-detection $ python detect.py
```

**\*\*\*Try each of the following four examples in the `openCV-examples`, include screenshots of your use and write about one design for each example that might work based on the individual benefits to each algorithm.\*\*\***


Contours-Detection


For the contour-detection example, one design use-case we saw fit would be an automatic vacuum (similar to a roomba). This algorithm would benefit this design the most for it would be able to detect the borders of different types of objects and be able to navigate around the object without interfering with it. 



<img width="1043" alt="Screen Shot 2022-10-24 at 8 09 10 PM" src="https://user-images.githubusercontent.com/111994216/197673042-c3665b69-8a64-4432-928d-2bd6f9e17884.png">




Face-Detection


For the facial recognition example, one design we believe is a benefit of this algorithm is a mask recognition application. This idea will identify if people entering a room have a mask on their face or if the mask is not on like seen above. The user would be notified if they can enter with their mask securely on or will notify the user to put a mask on before entering the room.


<img width="1079" alt="Screen Shot 2022-10-24 at 8 13 41 PM" src="https://user-images.githubusercontent.com/111994216/197673063-c32e5875-b77f-4bdc-8ca8-eb1214823056.png">




Optical Flow

For optical flow, this could be used to collect data on the flow of people or traffic. One thing I can think of is if we mounted the camera looking between the intersection of the house, Tata and Bloomberg, it could give a visualization of seeing what classes are beginning and ending judging from how people move between the buildings.

<img width="779" alt="Screen Shot 2022-10-24 at 11 05 40 PM" src="https://user-images.githubusercontent.com/111994216/197673155-dc25b8c6-9336-4751-bd6f-ac63c0e3c0e4.png">


Object-Detection

<img width="775" alt="Screen Shot 2022-10-24 at 11 05 32 PM" src="https://user-images.githubusercontent.com/111994216/197673370-9a44d52f-89e4-4c92-87b6-8a1a452bd4ec.png">


For the object detection one, we could make a type of sorting robot. It would identify the sizes of different objects in the room, and use that to move things so that they are arranged in order of size, or however the user specifies.

#### Filtering, FFTs, and Time Series data. 
Additional filtering and analysis can be done on the sensors that were provided in the kit. For example, running a Fast Fourier Transform over the IMU or Microphone data stream could create a simple activity classifier between walking, running, and standing.

To get the microphone working we need to install two libraries. `PyAudio` to get the data from the microphone, `sciPy` to make data analysis easy, and the `numpy-ringbuffer` to keep track of the last ~1 second of audio. 
Pyaudio needs to be installed with the following comand:
``sudo apt install python3-pyaudio``
SciPy is installed with 
``sudo apt install python3-scipy`` 

Lastly we need numpy-ringbuffer, to make continues data anlysis easier.
``pip install numpy-ringbuffer``

Now try the audio processing example:
* Find what ID the micrpohone has with `python ListAvalibleAudioDevices.py`
    Look for a device name that includes `USB` in the name.
* Adjust the variable `DEVICE_INDEX` in the `ExampleAudioFFT.py` file.
    See if you are getting results printed out from the microphone. Try to understand how the code works.
    Then run the file by typing `python ExampleAudioFFT.py`



Using the microphone, try one of the following:

**1. Set up threshold detection** Can you identify when a signal goes above certain fixed values?
Yes using code listed below, was able to see in output when signal went over the threshold

**2. Set up a running averaging** Can you set up a running average over one of the variables that are being calculated.[moving average](https://en.wikipedia.org/wiki/Moving_average)

**3. Set up peak detection** Can you identify when your signal reaches a peak and then goes down?

For technical references:

* Volume Calculation with [RootMeanSqare](https://en.wikipedia.org/wiki/Root_mean_square)
* [RingBuffer](https://en.wikipedia.org/wiki/Circular_buffer)
* [Frequency Analysis](https://en.wikipedia.org/wiki/Fast_Fourier_transform)


**\*\*\*Include links to your code here, and put the code for these in your repo--they will come in handy later.\*\*\***
Added a simple if statement to check the thresholds on volume. 
```
                print("Loudest Frqeuncy:",LoudestFrequency)
                print("RMS volume:",volumneSlow)
                print("Volume Change:",volumechange)

                if volumneSlow > 300:
                    print("high volume!!") # here
```

### (Optional Reading) Introducing Additional Concepts
The following sections ([MediaPipe](#mediapipe) and [Teachable Machines](#teachable-machines)) are included for your own optional learning. **The associated scripts will not work on Fall 2022's Pi Image, so you can move onto part B.** However, you are welcome to try it on your personal computer. If this functionality is desirable for your lab or final project, we can help you get a different image running the last OS and version of python to make the following code work.

#### MediaPipe

A more recent open source and efficient method of extracting information from video streams comes out of Google's [MediaPipe](https://mediapipe.dev/), which offers state of the art face, face mesh, hand pose, and body pose detection.

![Alt Text](mp.gif)

To get started, create a new virtual environment with special indication this time:

```
pi@ixe00:~ $ virtualenv mpipe --system-site-packages
pi@ixe00:~ $ source mpipe/bin/activate
(mpipe) pi@ixe00:~ $ 
```

and install the following.

```
...
(mpipe) pi@ixe00:~ $ sudo apt install ffmpeg python3-opencv
(mpipe) pi@ixe00:~ $ sudo apt install libxcb-shm0 libcdio-paranoia-dev libsdl2-2.0-0 libxv1  libtheora0 libva-drm2 libva-x11-2 libvdpau1 libharfbuzz0b libbluray2 libatlas-base-dev libhdf5-103 libgtk-3-0 libdc1394-22 libopenexr25
(mpipe) pi@ixe00:~ $ pip3 install mediapipe-rpi3 pyalsaaudio
```

Each of the installs will take a while, please be patient. After successfully installing mediapipe, connect your webcam to your Pi and use **VNC to access to your Pi**, open the terminal, and go to Lab 5 folder and run the hand pose detection script we provide:
(***it will not work if you use ssh from your laptop***)


```
(mpipe) pi@ixe00:~ $ cd Interactive-Lab-Hub/Lab\ 5
(mpipe) pi@ixe00:~ Interactive-Lab-Hub/Lab 5 $ python hand_pose.py
```

Try the two main features of this script: 1) pinching for percentage control, and 2) "[Quiet Coyote](https://www.youtube.com/watch?v=qsKlNVpY7zg)" for instant percentage setting. Notice how this example uses hardcoded positions and relates those positions with a desired set of events, in `hand_pose.py` lines 48-53. 

~~\*\*\*Consider how you might use this position based approach to create an interaction, and write how you might use it on either face, hand or body pose tracking.\*\*\*~~

(You might also consider how this notion of percentage control with hand tracking might be used in some of the physical UI you may have experimented with in the last lab, for instance in controlling a servo or rotary encoder.)



#### Teachable Machines
Google's [TeachableMachines](https://teachablemachine.withgoogle.com/train) might look very simple. However, its simplicity is very useful for experimenting with the capabilities of this technology.

![Alt Text](tm.gif)

To get started, create and activate a new virtual environment for this exercise with special indication:

```
pi@ixe00:~ $ virtualenv tmachine --system-site-packages
pi@ixe00:~ $ source tmachine/bin/activate
(tmachine) pi@ixe00:~ $ 
```

After activating the virtual environment, install the requisite TensorFlow libraries by running the following lines:
```
(tmachine) pi@ixe00:~ $ cd Interactive-Lab-Hub/Lab\ 5
(tmachine) pi@ixe00:~ Interactive-Lab-Hub/Lab 5 $ sudo chmod +x ./teachable_machines.sh
(tmachine) pi@ixe00:~ Interactive-Lab-Hub/Lab 5 $ ./teachable_machines.sh
``` 

This might take a while to get fully installed. After installation, connect your webcam to your Pi and use **VNC to access to your Pi**, open the terminal, and go to Lab 5 folder and run the example script:
(***it will not work if you use ssh from your laptop***)

```
(tmachine) pi@ixe00:~ Interactive-Lab-Hub/Lab 5 $ python tm_ppe_detection.py
```


(**Optionally**: You can train your own model, too. First, visit [TeachableMachines](https://teachablemachine.withgoogle.com/train), select Image Project and Standard model. Second, use the webcam on your computer to train a model. For each class try to have over 50 samples, and consider adding a background class where you have nothing in view so the model is trained to know that this is the background. Then create classes based on what you want the model to classify. Lastly, preview and iterate, or export your model as a 'Tensorflow' model, and select 'Keras'. You will find an '.h5' file and a 'labels.txt' file. These are included in this labs 'teachable_machines' folder, to make the PPE model you used earlier. You can make your own folder or replace these to make your own classifier.)

~~**\*\*\*Whether you make your own model or not, include screenshots of your use of Teachable Machines, and write how you might use this to create your own classifier. Include what different affordances this method brings, compared to the OpenCV or MediaPipe options.\*\*\***~~


*Don't forget to run ```deactivate``` to end the Teachable Machines demo, and to reactivate with ```source tmachine/bin/activate``` when you want to use it again.*


### Part B
### Construct a simple interaction.

* Pick one of the models you have tried, and experiment with prototyping an interaction.

Facial Recognition tracking

* This can be as simple as the boat detector shown in a previous lecture from Nikolas Matelaro.

* Try out different interaction outputs and inputs.
* Fill out the ``Contextual Interaction Design Tool`` sheet.[Found here.](ThinkingThroughContextandInteraction.png)

**\*\*\*Describe and detail the interaction, as well as your experimentation here.\*\*\***

The interaction we have decided to go further with was the mask detector application. This interaction would go as a user would walk up to a camera before entering a room or area, such as a classroom or airplane, and the sensor would detect if the user is wearing a proper face mask or if they did not have one on. If the latter, the user would be prompted to put on a mask before entering the room. 

<img width="775" alt="Mask detecting robot" src="https://media.timeout.com/images/105659495/image.jpg">


### Part C
### Test the interaction prototype

Now flight test your interactive prototype and **note down your observations**:
For example:
1. When does it what it is supposed to do?
When the user is not wearing a mask, it will say “NO MASK” and the user will know they need to put on a mask. 
When a user is wearing a mask, it will say “MASK ON, PROCEED”, and the user can enter the area

1. When does it fail?
Application fails when it can’t detect a face at all.
Application fails when it detects a face correctly but does not identify a mask correctly.

1. When it fails, why does it fail?
Can fail to detect faces due to poor lighting.
Application can fail if object or camera is in motion
Application can not differentiate between people of color.
Applications will only identify people of color without a mask or glasses.
Application has problems identifying objects that aren’t masks on someones face.

1. Based on the behavior you have seen, what other scenarios could cause problems?
Scenarios that have a combination of these will likely cause problems, so perhaps somewhat bad lighting with someone with glasses would probably cause a problem.
Do they have a very thick beard where a mask would usually be placed?
Do they have the mask partially on?
Are they wearing a mask with a face on it?

**\*\*\*Think about someone using the system. Describe how you think this will work.\*\*\***
1. Are they aware of the uncertainties in the system?
There are some systems that use facial recognition (such as Apple FaceID) and people would likely be familiar with those systems. 
So they will likely try small changes in order to make the system work (adjusting lighting, moving slowly, removing glasses, etc).

1. How bad would they be impacted by a miss classification?

Ideally there is human verification to help reinforce the results. So in most situations not so bad, as there would be a human monitor.
In situations where there is no monitor there would be bad reprecussions in the potential exposure of others.
Likely the worst if a company is using this, then it enters potential legal repercussions.

1. How could change your interactive system to address this?

Take different angles of pictures, adding to our sample for ml model.
Have a light built into the system that takes different pictures with varying light levels.
Asking the user to speak to see if an open mouth can be detected.

1. Are there optimizations you can try to do on your sense-making algorithm.

The algorithm could take advantage of more than just 1 photo for trying to get better and more accurate results. It could take pictures from multiple angles to get better results. It could utilize changes in lighting to enhance the quality of the photo. We could do this by adding a flash, or using different types of flashes. Also the device could ask the person to respond to a question, requiring them to open their mouth, which could help. We could also screen people where the algorithm did not give a conclusive answer, like “uncertain”.


### Part D
### Characterize your own Observant system

Now that you have experimented with one or more of these sense-making systems **characterize their behavior**. During the lecture, we mentioned questions to help characterize a material:
* What can you use X for?
X can be used to screen people if they are wearing a mask or not. It could provide a means to quickly process people and screen people with no masks or where the system has uncertainty.
Examples would be students entering schools, people entering events, people taking flights, people checking into a hotel at after hours, etc.

* What is a good environment for X?
In a well lit environment, and somewhere where the pi’s camera has a good, clear view of the person it is working with. Also the person does not have glasses or anything else that slightly blocks the users face.

* What is a bad environment for X?
A bad environment is a poorly lit environment, since pictures taken by the pi will not be able to really see the person it is trying to work with. Also if the pi is mounted in a bad position such that it gets only bad angles of the person. This would hinder its ability to determine if the person is wearing a mask.

* When will X break?

It breaks if the camera gets broken or obstructed. Since the majority of the functionality is reliant on the feed from the camera, if the camera gets hit or knocked off, this directly will affect the data the system uses to classify. Also if the camera just moves, this could have a large effect on the input data. Also if the camera is in motion or there is bad lighting, this negatively affects the output.

* When it breaks how will X break?
It will break if lighting is poor in the room or the user is in motion, it will incorrectly assume if a user has a mask on or off. The application will say put on a mask to the user even if user is already wearing a mask and vice versa. 


* What are other properties/behaviors of X?

Unfortunately X has a bias towards people of color and cannot as easily identify their faces. In our tests, people of color needed to have a very clear image (good lighting) without any face obstructions (such as glasses). 
We were unable to test with someone having a full beard, but we imagine it might have issues identifying them properly.

* How does X feel?
X feels a bit ineffective compared to a humans’ ability to quickly identify those wearing masks, but in a setting where human workforce is not available it provides a useful solution. X also feels ineffective due to its bias against people of color.

**\*\*\*Include a short video demonstrating the answers to these questions.\*\*\***

### Part 2.

Following exploration and reflection from Part 1, finish building your interactive system, and demonstrate it in use with a video.

**\*\*\*Include a short video demonstrating the finished result.\*\*\***



https://user-images.githubusercontent.com/111994216/197673931-b60acc04-5812-4046-b693-843c1f77e843.mov

