# Django Ninja vs DRF

O mesmo recurso — doações de uma igreja — exposto por **Django Ninja** e por **Django REST
Framework**, no mesmo projeto Django, sobre os mesmos models e o mesmo service.

A ideia é que a diferença entre `apps/donation/ninja_api/` e `apps/donation/drf_api/` seja **só
o framework**. Regra de negócio, escopo de dados e persistência ficam fora das duas bordas.

## Rodando

```bash
uv venv --python 3.12 .venv          # ou: python3.12 -m venv .venv
uv pip install -r requirements-dev.txt   # ou: .venv/bin/pip install -r requirements-dev.txt

.venv/bin/python manage.py migrate
.venv/bin/python manage.py seed_demo     # imprime um token Bearer por usuário
.venv/bin/python manage.py runserver
```

| | Django Ninja | DRF |
|---|---|---|
| Base | `/ninja/v1/` | `/drf/v1/` |
| Swagger | `/ninja/v1/docs` | `/drf/v1/docs` |
| OpenAPI | `/ninja/v1/openapi.json` | `/drf/v1/openapi.json` |

```bash
curl localhost:8000/ninja/v1/donation/ -H "Authorization: Bearer <token>"
curl localhost:8000/drf/v1/donation/   -H "Authorization: Bearer <token>"
```

Usuários do `seed_demo`:

- `church-user` — vê só as doações da própria igreja
- `regional-user` — vê as doações de todas as igrejas da sua regional
- `admin` — vê tudo (senha `admin`, também entra no `/admin/`)

## Endpoints

| Método | Rota | Regra |
|---|---|---|
| `GET` | `/donation/` | lista paginada (`limit`/`offset`), filtros `status`, `method`, `tertiarygroup_id` |
| `GET` | `/donation/{id}/` | 404 se a doação estiver fora do escopo do usuário |
| `POST` | `/donation/` | cria como `pending`; 400 se a igreja estiver fora do escopo |
| `POST` | `/donation/{id}/cancel/` | só cancela `pending`; 409 caso contrário |

## Onde comparar

| Assunto | Django Ninja | DRF |
|---|---|---|
| Registro das rotas | `config/api_ninja.py` | `config/api_drf.py` |
| Rotas / views | `apps/donation/ninja_api/router.py` | `apps/donation/drf_api/views.py` |
| Contrato de entrada e saída | `apps/donation/ninja_api/schemas.py` | `apps/donation/drf_api/serializers.py` |
| Filtros | `apps/donation/ninja_api/filters.py` | `apps/donation/drf_api/filters.py` |
| Autenticação | `misc/ninja/auth.py` | `misc/drf/authentication.py` |
| Escopo por usuário | chamado em cada rota | `misc/drf/mixins.py` (`get_queryset`) |
| Erro de regra de negócio → HTTP | `@api.exception_handler` em `config/api_ninja.py` | `misc/drf/exception_handler.py` |
| Configuração global | argumentos do `NinjaAPI(...)` | `REST_FRAMEWORK` em `config/settings.py` |

Compartilhado pelas duas bordas:

- `apps/donation/services/donation_service.py` — as regras (escopo da igreja, só cancela `pending`)
- `apps/group/querysets.py`, `apps/donation/querysets.py` — o que cada usuário enxerga
- `apps/donation/exceptions.py`, `misc/exceptions.py` — erros de domínio, sem HTTP

## Diferenças que aparecem rodando

Todas cobertas por `apps/donation/tests/test_donation_api.py`: a mesma suíte
(`DonationApiContract`) roda contra as duas bordas, e o que muda entre elas fica declarado nas
duas subclasses.

| | Django Ninja | DRF |
|---|---|---|
| Payload inválido | **422** | **400** |
| Envelope da paginação | `{items, count}` | `{count, next, previous, results}` |
| Datas na resposta | UTC, milissegundos (`...329Z`) | fuso local, microssegundos (`...329581-03:00`) |
| Bearer no OpenAPI | automático (`HttpBearer`) | precisa de `OpenApiAuthenticationExtension` |
| Create chamando service | rota comum | sobrescreve `create`; o `CreateModelMixin` espera `serializer.save()` |

## Testes e lint

```bash
.venv/bin/pytest
.venv/bin/ruff check . && .venv/bin/ruff format --check .
```

## Versões

Python 3.12, Django 5.2, Django Ninja 1.7, DRF 3.18, drf-spectacular 0.30. SQLite, para rodar
sem infraestrutura.
# django-ninja-vs-drf
