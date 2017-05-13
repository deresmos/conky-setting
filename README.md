conky-setting
==
Create conky conf that automatically generated according to the environment and run conky script.

* Example desktop image
![Desktop picture](./desktop.png "desktop")

Setting
--
* Change conf files
	* Set variable `conf_names` like `['info', 'system']` in start.py


Usage
--
* Create and update conky conf.
```sh
python start.py
```

* Create conky conf and run conky.
```sh
python start.py 1
```

* Run conky.
```sh
python start.py 2
```


License
--
Released under the MIT license, see LICENSE.
