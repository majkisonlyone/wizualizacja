# SETUP

1. Install python dependencies from `requirements.txt`
    ```
    python3 -m venv ../venv_wizualizacja
    chmod +x ../venv_wizualizacja/bin/activate
    source ../venv_wizualizacja/bin/activate
    pip install -r requirements.txt
    ```

2. Install `freeglut3-dev`
    ```
    sudo apt-get install freeglut3-dev
    ```

3. Be aware that there is a known bug in OpenGL working on Wayland:
    - https://github.com/pygame/pygame/issues/3110

    - WA: comment out [this line](https://github.com/mcfletch/pyopengl/blob/29b79e8966ba2930a5c44829b02dffc1ca600752/OpenGL/contextdata.py#L38) ass suggested by [this WA](https://github.com/pygame/pygame/issues/3110#issuecomment-1746668102)

# USAGE

1. run `zad*` python files, eg:
    ```
    python3 zad4_1.py
    ```

# ADDITIONAL NOTES

1. `zad4_4.py` allows addition/deletion of figures, press:
    - `a` - to add new figure
    - `d` - to delete existing figure

2. `zad5_3.py` imports scene from file `file1.sci`
    - use `w` and `s` keys to move camera closer or farther
    - use `a` and `d` keys to rotate camera left/right
    - use `r` and `f` keys to rotate camera upwards/downwards