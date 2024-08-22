e108
===

Mais um projeto sem futuro  

Coméque
---

Copiar **example.env** pra **.env**. Tem que abrir o 
arquivo em um editor de texto e configurar do jeito certo.  

Criar um diretório de nome **instance** pro banco de dados (no futuro eu vou 
criar isto automaticamente no código)  

### pipenv

```
$ pipenv install --dev
$ pipenv run pw ## Site
$ pipenv run pa ## API
```

### venv / pip

```
$ python -m venv venv
$ source venv/bin/activate # Unix
$ .\venv\Scripts\activate # Powershell
(venv) $ pip install -e .
(venv) $ python -m e108 web ## Site
(venv) $ python -m e108 api ## API
```

Licença
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
