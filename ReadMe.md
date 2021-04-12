# RenderDoc extension to dump raw binary data of textures

Added an extension to read the binary data of a texture and dump it into a file.

Main use-case: when sending binary data to a shader as a texture and it gets corrupt in the driver level.

With this you can compare between the texture binary data you send to the shader vs the data the shader is actually using


## installation

if you use Linux or Cygwin in Windows you can run the install.sh to install the extension
if not you can follow these steps:
- copy the directory `raw_texture_dump` to `%APPDATA%\qrenderdoc\extensions\`
- start render doc and enabled the extension https://renderdoc.org/docs/how/how_python_extension.html#enabling-extensions
- then go to the TextureViewer panel when viewing the texture you want to export
- click the puzzel button in the Action Panel
- choose `Save Texture as Binary`

if you don't see `Save Texture as Binary` make sure you enabled the extension correctly
