# remove-background
A Blender addon that uses a U²-Net to automatically remove backgrounds of images and generate alpha masks. It also allows you to automatically color grade the subject image based on the background. 

## Demonstration:
Initial images (waterfall):
<img width="1920" height="791" alt="initial_images" src="https://github.com/user-attachments/assets/fea277c5-27ef-4d3c-a800-ac2abf2b426b" />

Result after removing background and overlaying:
<img width="1280" height="853" alt="demo2" src="https://github.com/user-attachments/assets/8f550b23-6674-4cb7-b4d7-3107bc1c97c3" />

Initial images (road):
<img width="1920" height="791" alt="initial_images1" src="https://github.com/user-attachments/assets/dfa68c57-8093-4d1b-863f-14592047b514" />

Result after removing background and overlaying:
<img width="1280" height="853" alt="demo1" src="https://github.com/user-attachments/assets/93d0c915-6242-4058-9efa-3a8a5be1bf36" />

## Installation Guide:

Download or clone the repository and install via Edit -> Preferences -> Addons -> Install from disk.
You *must* run Blender as administrator for this to work because this addon requires additional modules (torch, torchvision, PIL, openCV) and these will take a few minutes to download. (Open up the system console to view progress.)
The addon also sets permissions of the newly created 'modules' folder so you can use them with regular, non-admin Blender every time after the initial install. 

