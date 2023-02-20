# Canvis

- Millores de Docker:
  - Millora en el `Dockerfile`
  - Canvi en l'estructura del doc1ker
  - Afegit del `.env` en el root del projecte per poder tenir un sol `compose.yml` amb variables de desenvolupament i preproducció (weak feature, potencialment no sigui d'utilitat tampoc)
  - Afegit el `.dockerignore` per reduïr la mida de la imatge en producció i millorar la seguretat al no exposar potencials secrets
- Modificada la configuració de flake8, black i isort (afegit el fitxer de `.flake8` per això)
- Eliminat `tox`. Raó: tox serveix per testejar en diferents plataformes, i això no ho necessitarem mai perquè nosaltres tenim contenidors (els quals sempre corren en el mateix sistema operatiu, el del contenidor)
- Eliminat `pytest`: de moment no el fem servir enlloc i jo he trobat que, per ara, fer servir el mòdul de tests built-in de Django ja va bé. Si això ho deixaria més a desició de la persona que aixeca el projecte si vol afegir pytest que no pas afegir-lo directament per treure'l.
- Afegits els scripts de `run` i `rename-project`. Run és un conjunt d’utilitats variades i rename-project és autodescriptiu. Potencialment en un futur `rename-project`podria ser subtituit pel cookiecutter en si (tot i que podria existir igual en cas que la persona s’hagi equivocat de nom o vulgui cnaviar-lo més endavant per qualsevol altra raó)
- Millora del [README.md](http://README.md "‌")
- Millora del `.gitignore`
- Afegits workflows pel github, subtituit el que teniem que feia correr tox per uns altres de més senzill que fan bàsicament el mateix més rapid. A més, afeigt un que testeja si el compose i dockerfile funcionen bé
- Afegit linter per la dockerfile `hadolint`
