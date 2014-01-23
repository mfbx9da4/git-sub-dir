Downloads git sub dir

##Usage
      

    python get_git_sub_dir.py path/to/sub/dir <RECURSIVE>
    
<RECURSIVE> is a boolen `True` or `False`. Default is `True`.


##Example

Lets download the docs from twitter bootstrap https://github.com/twbs/bootstrap/tree/master/docs

    python get_git_sub_dir.py twbs/bootstrap/docs

If we don't want it to be recursive

    python get_git_sub_dir.py twbs/bootstrap/docs False
