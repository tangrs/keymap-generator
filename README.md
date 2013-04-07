Linux keymap generator
======================

Generate a device tree compatible matrix keymap. Given an input, it will produce a list of integers in the format of: ```row << 24 | col << 16 | keycode```.

Input format
------------

Input is a file containing a whitespace separated table of keycodes. They may be hardcoded or may use defines from include/uapi/linux/input.h (http://lxr.free-electrons.com/source/include/uapi/linux/input.h).

The table begins with the ```===begin===``` marker and ends with the ```===end===``` marker.

Whitespace separates columns and newlines separate rows.

Table will match the keymaps at http://hackspire.unsads.com/wiki/index.php/Keypads (i.e. offset 0x0010, bit 0 references row 0, column 0, offset 0x0010, bit 1 references row 0, column 1 etc...).

Program usage
-------------

```python keymap_maker.py input.txt /path/to/linux-2.6```

It needs the kernel source code directory for the ```input.h``` header to resolve the defines. It runs the C preprocessor defined in the ```CPP``` variable of the script to process the keymap.


