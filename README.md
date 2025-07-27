# remove-background
<img width="1280" height="854" alt="final" src="https://github.com/user-attachments/assets/2e8339c7-8cd4-4369-8fb1-ae5d03cfd2b0" />

A Blender addon that uses a U²-Net to automatically remove backgrounds of images and generate alpha masks. It also allows you to automatically color grade the subject image based on the background. 

## Demo Video:


https://github.com/user-attachments/assets/1e50b468-a6d8-40fa-9aa2-ea1894990b04


## Result Images:
Initial images (waterfall):
<img width="1920" height="791" alt="initial_images" src="https://github.com/user-attachments/assets/fea277c5-27ef-4d3c-a800-ac2abf2b426b" />

Result after removing background and overlaying:
<img width="1280" height="853" alt="demo2" src="https://github.com/user-attachments/assets/8f550b23-6674-4cb7-b4d7-3107bc1c97c3" />

Initial images (road):
<img width="1920" height="791" alt="initial_images1" src="https://github.com/user-attachments/assets/dfa68c57-8093-4d1b-863f-14592047b514" />

Result after removing background and overlaying:
<img width="1280" height="853" alt="demo1" src="https://github.com/user-attachments/assets/93d0c915-6242-4058-9efa-3a8a5be1bf36" />

## Installation Guide:

- Download or clone the repository and install via Edit -> Preferences -> Addons -> Install from disk.
- You *must* run Blender as administrator for this to work because this addon requires additional modules (torch, torchvision, PIL, openCV) and these will take a few minutes to download. (Open up the system console to view progress.)
- The addon also sets permissions of the newly created 'modules' folder so you can use them with regular, non-admin Blender every time after the initial install.

  ## Credits
  - Original U²-Net Paper: https://github.com/xuebinqin/U-2-Net/tree/master
  - Usage of model inspired by: https://github.com/Nkap23/u2net_bgremove_code/tree/main
  - Reinhard color transfer algorithm by <a href="https://www.researchgate.net/publication/220518215_Color_Transfer_between_Images"> Reinhard, Erik & Ashikhmin, Michael & Gooch, Bruce & Shirley, Peter. (2001). Color Transfer between Images. IEEE Computer Graphics and Applications. 21. 34-41. 10.1109/38.946629.</a>
  - Woman in a red dress image by <a href="https://pixabay.com/users/surprising_media-11873433/?utm_source=link-attribution&utm_medium=referral&utm_campaign=image&utm_content=6576618">Mircea Iancu</a> from <a href="https://pixabay.com//?utm_source=link-attribution&utm_medium=referral&utm_campaign=image&utm_content=6576618">Pixabay</a>
  - Waterfall image by <a href="https://pixabay.com/users/renegossner-10236719/?utm_source=link-attribution&utm_medium=referral&utm_campaign=image&utm_content=6473754">Rene Gossner</a> from <a href="https://pixabay.com//?utm_source=link-attribution&utm_medium=referral&utm_campaign=image&utm_content=6473754">Pixabay</a>
  - Road image by <a href="https://pixabay.com/users/ryanmcguire-123690/?utm_source=link-attribution&utm_medium=referral&utm_campaign=image&utm_content=238458">Ryan McGuire</a> from <a href="https://pixabay.com//?utm_source=link-attribution&utm_medium=referral&utm_campaign=image&utm_content=238458">Pixabay</a>

