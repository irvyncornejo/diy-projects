#!/usr/bin/env bash
# ============================================================
#  new-diy-project.sh  v2.1
#  Genera la estructura estándar para un proyecto DIY de Irvyn
#  Uso: ./new-diy-project.sh
#  Fix v2.1: exec </dev/tty tras el BOM loop para evitar que
#            el Enter vacío consuma BASE_DIR y CONFIRM
# ============================================================

set -euo pipefail

# ── Colores ──────────────────────────────────────────────────────
C_RESET="\033[0m"; C_BOLD="\033[1m"; C_RED="\033[0;31m"
C_GREEN="\033[0;32m"; C_YELLOW="\033[1;33m"; C_CYAN="\033[0;36m"
C_PURPLE="\033[0;35m"

echo -e "${C_CYAN}${C_BOLD}
  ┌─────────────────────────────────────────────┐
  │         DIY Project Initializer v2.1        │
  │            by Irvyn Sánchez                 │
  └─────────────────────────────────────────────┘
${C_RESET}"

# ── Info básica ───────────────────────────────────────────────────
echo -e "${C_BOLD}── Información del proyecto ──────────────────────────────${C_RESET}\n"

read -rp "$(echo -e ${C_CYAN})Nombre del proyecto (ej: desk-setup-hmi): $(echo -e ${C_RESET})" PROJECT_NAME
PROJECT_NAME="${PROJECT_NAME// /-}"
PROJECT_NAME=$(echo "$PROJECT_NAME" | tr '[:upper:]' '[:lower:]')

read -rp "$(echo -e ${C_CYAN})Título legible (ej: Desk Setup HMI): $(echo -e ${C_RESET})" PROJECT_TITLE

# ── Dificultad ────────────────────────────────────────────────────
echo -e "\n${C_BOLD}Dificultad:${C_RESET}"
echo "  1) beginner"; echo "  2) intermediate"; echo "  3) advanced"
read -rp "$(echo -e ${C_CYAN})Selecciona [1-3]: $(echo -e ${C_RESET})" DIFF_OPT
case "$DIFF_OPT" in
  1) DIFFICULTY="beginner" ;;
  3) DIFFICULTY="advanced" ;;
  *) DIFFICULTY="intermediate" ;;
esac

# ── Plataforma ────────────────────────────────────────────────────
echo -e "\n${C_BOLD}Plataforma:${C_RESET}"
echo "  1) arduino"; echo "  2) raspberry-pi-pico"
echo "  3) esp32";   echo "  4) raspberry-pi"; echo "  5) other"
read -rp "$(echo -e ${C_CYAN})Selecciona [1-5]: $(echo -e ${C_RESET})" PLATFORM_OPT
case "$PLATFORM_OPT" in
  1) PLATFORM="arduino" ;;
  2) PLATFORM="raspberry-pi-pico" ;;
  3) PLATFORM="esp32" ;;
  4) PLATFORM="raspberry-pi" ;;
  *) PLATFORM="other" ;;
esac

# ── Categoría ─────────────────────────────────────────────────────
echo -e "\n${C_BOLD}Categoría:${C_RESET}"
echo "  1) HMI";       echo "  2) IoT";     echo "  3) Automation"
echo "  4) Macro-key"; echo "  5) Control"; echo "  6) Game"; echo "  7) Other"
read -rp "$(echo -e ${C_CYAN})Selecciona [1-7]: $(echo -e ${C_RESET})" CATEGORY_OPT
case "$CATEGORY_OPT" in
  1) CATEGORY="hmi" ;;
  2) CATEGORY="iot" ;;
  3) CATEGORY="automation" ;;
  4) CATEGORY="macro-key" ;;
  5) CATEGORY="control" ;;
  6) CATEGORY="game" ;;
  *)
    read -rp "$(echo -e ${C_CYAN})Ingresa la categoría personalizada: $(echo -e ${C_RESET})" CATEGORY_CUSTOM
    CATEGORY=$(echo "$CATEGORY_CUSTOM" | tr '[:upper:]' '[:lower:]')
    ;;
esac

# ── Descripción, autor y tags ─────────────────────────────────────
echo ""
read -rp "$(echo -e ${C_CYAN})Descripción corta del proyecto: $(echo -e ${C_RESET})" DESCRIPTION
read -rp "$(echo -e ${C_CYAN})Tu nombre de autor [Irvyn Sánchez]: $(echo -e ${C_RESET})" AUTHOR
AUTHOR="${AUTHOR:-Irvyn Sánchez}"
read -rp "$(echo -e ${C_CYAN})Tags separados por coma (ej: iot,hmi,pico): $(echo -e ${C_RESET})" TAGS_RAW

# ── Lenguaje ──────────────────────────────────────────────────────
echo -e "\n${C_BOLD}Lenguaje principal:${C_RESET}"
echo "  1) python / micropython"; echo "  2) c / arduino"
echo "  3) circuitpython";        echo "  4) mixed"
read -rp "$(echo -e ${C_CYAN})Selecciona [1-4]: $(echo -e ${C_RESET})" LANG_OPT
case "$LANG_OPT" in
  1) LANGUAGE="python" ;;
  2) LANGUAGE="c" ;;
  3) LANGUAGE="circuitpython" ;;
  *) LANGUAGE="mixed" ;;
esac

# ── Bill of Materials (BOM) ───────────────────────────────────────
echo -e "\n${C_PURPLE}── Bill of Materials (BOM) ───────────────────────────────${C_RESET}"
echo -e "${C_YELLOW}  Ingresa los componentes uno por uno.
  Para cada componente puedes agregar links de compra.
  Deja en blanco el nombre para terminar.${C_RESET}\n"

BOM_YAML=""
BOM_CSV="qty,component,description,unit_price_mxn,buy_amazon,buy_aliexpress,buy_other\n"
BOM_README=""
BOM_COUNT=0

while true; do
  read -rp "$(echo -e ${C_CYAN})  Componente #$((BOM_COUNT+1)) — Nombre (Enter para terminar): $(echo -e ${C_RESET})" COMP_NAME
  [ -z "$COMP_NAME" ] && break

  read -rp "$(echo -e ${C_CYAN})    Descripción breve: $(echo -e ${C_RESET})"                       COMP_DESC
  read -rp "$(echo -e ${C_CYAN})    Cantidad [1]: $(echo -e ${C_RESET})"                             COMP_QTY
  COMP_QTY="${COMP_QTY:-1}"
  read -rp "$(echo -e ${C_CYAN})    Precio unitario MXN estimado (ej: 3.50) [0]: $(echo -e ${C_RESET})" COMP_PRICE
  COMP_PRICE="${COMP_PRICE:-0}"

  echo -e "    ${C_YELLOW}Links de compra (opcional — Enter para omitir):${C_RESET}"
  read -rp "$(echo -e ${C_CYAN})    Amazon URL: $(echo -e ${C_RESET})"                               LINK_AMAZON
  read -rp "$(echo -e ${C_CYAN})    AliExpress URL: $(echo -e ${C_RESET})"                           LINK_ALI
  read -rp "$(echo -e ${C_CYAN})    Otro link (Tindie / DigiKey / local): $(echo -e ${C_RESET})"    LINK_OTHER

  BOM_YAML+="  - name: \"${COMP_NAME}\"\n"
  BOM_YAML+="    description: \"${COMP_DESC}\"\n"
  BOM_YAML+="    qty: ${COMP_QTY}\n"
  BOM_YAML+="    unit_price_mxn: ${COMP_PRICE}\n"
  BOM_YAML+="    buy_links:\n"
  [ -n "$LINK_AMAZON" ] && BOM_YAML+="      amazon: \"${LINK_AMAZON}\"\n"
  [ -n "$LINK_ALI"    ] && BOM_YAML+="      aliexpress: \"${LINK_ALI}\"\n"
  [ -n "$LINK_OTHER"  ] && BOM_YAML+="      other: \"${LINK_OTHER}\"\n"

  BOM_CSV+="${COMP_QTY},\"${COMP_NAME}\",\"${COMP_DESC}\",${COMP_PRICE},\"${LINK_AMAZON}\",\"${LINK_ALI}\",\"${LINK_OTHER}\"\n"

  LINKS_MD="| ${COMP_QTY} | **${COMP_NAME}** | ${COMP_DESC} | \$${COMP_PRICE} |"
  [ -n "$LINK_AMAZON" ] && LINKS_MD+=" [Amazon](${LINK_AMAZON})"
  [ -n "$LINK_ALI"    ] && LINKS_MD+=" [AliExpress](${LINK_ALI})"
  [ -n "$LINK_OTHER"  ] && LINKS_MD+=" [Otro](${LINK_OTHER})"
  [ -z "${LINK_AMAZON}${LINK_ALI}${LINK_OTHER}" ] && LINKS_MD+=" —"
  BOM_README+="${LINKS_MD} |\n"

  BOM_COUNT=$((BOM_COUNT+1))
  echo ""
done

# ── Costo total estimado ──────────────────────────────────────────
TOTAL_COST=0
if [ "$BOM_COUNT" -gt 0 ]; then
  TOTAL_COST=$(echo -e "$BOM_YAML" | awk '
    /qty:/ { qty = $2 }
    /unit_price_mxn:/ { price = $2; total += qty * price }
    END { print total + 0 }
  ')
fi

# ── Directorio destino ────────────────────────────────────────────
echo -e "\n${C_BOLD}Directorio base donde crear el proyecto:${C_RESET}"
dirs=(".")
for d in */; do
  if [ -d "$d" ]; then
    dirname="${d%/}"
    # Excluir directorios especiales ocultos o estándar del repositorio
    if [[ "$dirname" != "tests" && "$dirname" != "docs" && "$dirname" != "assets" && "$dirname" != "hmi" && "$dirname" != "code" && "$dirname" != "node_modules" && ! "$dirname" =~ ^\..* ]]; then
      dirs+=("$dirname")
    fi
  fi
done

for i in "${!dirs[@]}"; do
  echo "  $i) ${dirs[$i]}"
done

read -rp "$(echo -e ${C_CYAN})Selecciona el directorio [0-$((${#dirs[@]}-1))] [0]: $(echo -e ${C_RESET})" DIR_OPT
DIR_OPT="${DIR_OPT:-0}"

if [[ "$DIR_OPT" =~ ^[0-9]+$ ]] && [ "$DIR_OPT" -lt "${#dirs[@]}" ]; then
  BASE_DIR="${dirs[$DIR_OPT]}"
else
  BASE_DIR="."
fi
BASE_DIR="${BASE_DIR%/}"

PROJECT_PATH="${BASE_DIR}/${PROJECT_NAME}"
DATE_NOW=$(date +"%Y-%m-%d")

# ── Resumen ───────────────────────────────────────────────────────
echo -e "\n${C_YELLOW}${C_BOLD}── Resumen ────────────────────────────────────────────${C_RESET}"
echo -e "  Proyecto  : ${C_BOLD}${PROJECT_TITLE}${C_RESET}"
echo -e "  Slug      : ${PROJECT_NAME}"
echo -e "  Ruta      : ${C_BOLD}${PROJECT_PATH}${C_RESET}"
echo -e "  Platform  : ${PLATFORM}"
echo -e "  Categoría : ${CATEGORY}"
echo -e "  Dificultad: ${DIFFICULTY}"
echo -e "  Lenguaje  : ${LANGUAGE}"
echo -e "  Componentes BOM: ${BOM_COUNT}"
[ "$BOM_COUNT" -gt 0 ] && echo -e "  Costo estimado: \$${TOTAL_COST} MXN"
echo ""

read -rp "$(echo -e ${C_CYAN})¿Confirmar y crear proyecto? [s/N]: $(echo -e ${C_RESET})" CONFIRM
if [[ ! "$CONFIRM" =~ ^[sS]$ ]]; then
  echo -e "${C_RED}Cancelado.${C_RESET}"
  exit 0
fi

# ── Crear estructura de carpetas ──────────────────────────────────
echo -e "\n${C_GREEN}▶ Creando estructura de carpetas...${C_RESET}"
mkdir -p "${PROJECT_PATH}"/{docs,hmi,code,assets/{images,schematics,3d-files},tests}

# ── Tags YAML ─────────────────────────────────────────────────────
TAGS_YAML=""
IFS=',' read -ra TAG_ARR <<< "$TAGS_RAW"
for tag in "${TAG_ARR[@]}"; do
  tag="${tag// /}"
  [ -n "$tag" ] && TAGS_YAML+="  - \"${tag}\"\n"
done

# ── BOM bloque YAML ───────────────────────────────────────────────
if [ "$BOM_COUNT" -eq 0 ]; then
  BOM_FINAL="[]   # Añadir componentes con: name, qty, unit_price_mxn, buy_links"
else
  BOM_FINAL="$(echo -e "$BOM_YAML")"
fi

# ── Generar project.yml ───────────────────────────────────────────
echo -e "${C_GREEN}▶ Generando project.yml...${C_RESET}"
cat > "${PROJECT_PATH}/project.yml" <<YAML
# ──────────────────────────────────────────────────────────────────
#  project.yml  —  Metadata estándar para proyectos DIY
#  Generado automáticamente por new-diy-project.sh v2.1
# ──────────────────────────────────────────────────────────────────

project:
  name: "${PROJECT_NAME}"
  title: "${PROJECT_TITLE}"
  description: "${DESCRIPTION}"
  version: "0.1.0"
  status: "in-progress"          # draft | in-progress | stable | archived
  difficulty: "${DIFFICULTY}"    # beginner | intermediate | advanced
  created_at: "${DATE_NOW}"
  updated_at: "${DATE_NOW}"

author:
  name: "${AUTHOR}"
  github: "irvyncornejo"

hardware:
  platform: "${PLATFORM}"
  language: "${LANGUAGE}"
  category: "${CATEGORY}"

tags:
$(echo -e "$TAGS_YAML")
structure:
  has_hmi: true                  # Incluye pantalla/HMI Nextion?
  has_schematics: false          # Tiene diagramas de circuito?
  has_3d_files: false            # Tiene archivos STL/CAD?
  has_tests: false               # Incluye pruebas unitarias?

links:
  github: "https://github.com/irvyncornejo/diy-projects"
  demo_video: ""
  docs: ""

media:
  cover_image: "assets/images/cover.jpg"
  gallery: []

bom: ${BOM_FINAL}

notes: |
  Agregar notas del proyecto aqui...
YAML

# ── Generar assets/bom.csv ────────────────────────────────────────
if [ "$BOM_COUNT" -gt 0 ]; then
  printf "%b" "$BOM_CSV" > "${PROJECT_PATH}/assets/bom.csv"
fi

# ── Generar README.md ─────────────────────────────────────────────
echo -e "${C_GREEN}▶ Generando README.md...${C_RESET}"

if [ "$BOM_COUNT" -gt 0 ]; then
  BOM_TABLE="## 🛒 Bill of Materials\n\n| Qty | Componente | Descripción | Precio | Links |\n|-----|-----------|-------------|--------|-------|\n$(echo -e "$BOM_README")"
else
  BOM_TABLE="## 🛒 Bill of Materials\n\n_Completar en project.yml > bom_\n"
fi

cat > "${PROJECT_PATH}/README.md" <<README
# ${PROJECT_TITLE}

> ${DESCRIPTION}

![Status](https://img.shields.io/badge/status-in--progress-yellow)
![Platform](https://img.shields.io/badge/platform-${PLATFORM}-blue)
![Language](https://img.shields.io/badge/language-${LANGUAGE}-green)

## 📋 Descripción

<!-- Ampliar descripción aquí -->

## 🗂 Estructura

\`\`\`
${PROJECT_NAME}/
├── project.yml          # Metadata del proyecto
├── README.md
├── CHANGELOG.md
├── code/                # Código fuente
├── hmi/                 # Archivos .HMI (Nextion)
├── docs/                # Documentación
├── assets/
│   ├── images/          # Fotos y capturas
│   ├── schematics/      # Diagramas de circuito
│   └── 3d-files/        # Archivos STL/CAD
└── tests/
\`\`\`

$(echo -e "$BOM_TABLE")

## 🚀 Cómo empezar

1. Clona el repositorio
2. Revisa \`project.yml\` para el listado de componentes
3. Sube el código de \`code/\` a tu ${PLATFORM}

---
*Generado con new-diy-project.sh v2.1 — ${DATE_NOW}*
README

# ── Generar CHANGELOG.md ──────────────────────────────────────────
cat > "${PROJECT_PATH}/CHANGELOG.md" <<CHANGELOG
# Changelog — ${PROJECT_TITLE}

## [0.1.0] — ${DATE_NOW}
### Added
- Estructura inicial del proyecto
- project.yml con metadata
CHANGELOG

# ── Generar .gitignore ────────────────────────────────────────────
cat > "${PROJECT_PATH}/.gitignore" <<GITIGNORE
# Python
__pycache__/
*.pyc
*.pyo
.env
venv/

# macOS
.DS_Store
.AppleDouble

# IDEs
.vscode/
.idea/
*.swp

# Build
build/
dist/
*.bin
*.uf2
GITIGNORE

# ── Resumen final ─────────────────────────────────────────────────
echo -e "\n${C_GREEN}${C_BOLD}✔ Proyecto '${PROJECT_NAME}' creado exitosamente en:${C_RESET}"
echo -e "  ${C_BOLD}${PROJECT_PATH}${C_RESET}\n"
echo -e "${C_CYAN}Archivos generados:${C_RESET}"
find "${PROJECT_PATH}" | sed "s|${PROJECT_PATH}/||" | grep -v "^${PROJECT_PATH}$" | sort | \
  while IFS= read -r f; do
    depth=$(echo "$f" | tr -cd '/' | wc -c)
    indent=$(printf '%*s' $((depth * 2)) '')
    echo "  ${indent}├── $(basename "$f")"
  done

echo ""
echo -e "${C_YELLOW}Próximos pasos:${C_RESET}"
echo -e "  1. Edita ${PROJECT_NAME}/project.yml con los detalles finales"
echo -e "  2. Agrega tu código en code/"
echo -e "  3. Sube el .HMI a hmi/ si aplica"
[ "$BOM_COUNT" -eq 0 ] && echo -e "  4. Completa el BOM en project.yml > bom:"
