# General toolkit.
Odak provides a set of functions that can be used for general purpose work, such as saving an image file or loading a three-dimensional point cloud of an object.
These functions are helpful for general use and provide consistency across routine works in loading and saving routines.
When working with odak, we strongly suggest sticking to the general toolkit to provide a coherent solution to your task.

## Engineering notes

| Note          | Description   |
| ------------- |:-------------:|
| `Working with images` | This engineering note will give you an idea about how read and write images using odak. |

## odak.tools
This submodule is based on `numpy`. If you are using functions outside of `odak.learn` submodule, we recommend you to use this specific set of tools.
Note that there are also corner case like loading a dictionary when using `odak.learn`, which does not necessarily require to work with `odak.learn.tools` as `odak.tools.load_dictionary` works with `numpy`, `cupy` or `torch`.
In such cases, `odak.tools` is the go to submodule.

| Function      | Description   |
| ------------- |:-------------:|
| [odak.tools.check_directory](odak/tools/check_directory.md) | Check if directory exist, if not create it. |
| [odak.tools.load_image](odak/tools/load_image.md) | Load an image. |
| [odak.tools.load_dictionary](odak/tools/load_dictionary.md) | Load a dictionary. |
| [odak.tools.save_image](odak/tools/save_image.md) | Save as an image. |
| [odak.tools.save_dictionary](odak/tools/save_dictionary.md) | Save a dictionary. |
| [odak.tools.shell_command](odak/tools/shell_command.md) | Trigger a shell command. |