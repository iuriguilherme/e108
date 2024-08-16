e108
===

Mais um projeto sem futuro  

Coméque
---

Copiar **example.config.ini** pra **instance/config.ini**. Tem que abrir o 
arquivo em um editor de texto e configurar do jeito certo.  

Idem com **example.env** pra **.env**  

### pipenv

```
$ pipenv install -e .
$ pipenv run prod
```

### poetry

```
$ poetry install
$ poetry run prod
```

### venv / pip

```
$ python -m venv venv
$ source venv/bin/activate # Unix
$ .\venv\Scripts\activate # Powershell
(venv) $ pip install -e .
(venv) $ python -m e108
```

Licensa
---

Copyright 2024 Iuri Guilherme <https://iuri.neocities.org/>

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
MA 02110-1301, USA.
