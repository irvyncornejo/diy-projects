#!/usr/bin/env python3
import os
import sys
import csv
import re

def sync_project(project_dir):
    project_yml_path = os.path.join(project_dir, 'project.yml')
    bom_csv_path = os.path.join(project_dir, 'assets', 'bom.csv')
    readme_path = os.path.join(project_dir, 'README.md')

    if not os.path.exists(project_yml_path) or not os.path.exists(bom_csv_path):
        print(f"[-] Omitiendo {project_dir}: no contiene project.yml o assets/bom.csv")
        return False

    print(f"[*] Sincronizando BOM para: {project_dir} ...")

    # 1. Leer CSV
    bom_items = []
    try:
        with open(bom_csv_path, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            # Normalizar nombres de columnas por si acaso hay espacios
            reader.fieldnames = [name.strip() for name in reader.fieldnames] if reader.fieldnames else []
            for row in reader:
                # Limpiar valores
                item = {k: (v.strip() if v else "") for k, v in row.items()}
                if item.get('component'):
                    bom_items.append(item)
    except Exception as e:
        print(f"  [!] Error al leer CSV: {e}")
        return False

    if not bom_items:
        print("  [!] CSV vacío o no tiene componentes válidos.")
        return False

    # 2. Generar YAML para bom
    # Formato:
    # bom:
    #   - name: "..."
    #     description: "..."
    #     qty: 1
    #     unit_price_mxn: 5
    #     buy_links:
    #       other: "..."
    yaml_lines = ["bom:"]
    for item in bom_items:
        yaml_lines.append(f'  - name: "{item["component"]}"')
        yaml_lines.append(f'    description: "{item.get("description", "")}"')
        try:
            qty = int(item.get("qty", 1))
        except ValueError:
            qty = 1
        try:
            # Soporta tanto unit_price_mxn como unit_price_usd (retrocompatibilidad)
            raw_price = item.get("unit_price_mxn") or item.get("unit_price_usd") or "0"
            price = float(raw_price)
            # Formatear como entero si no tiene decimales
            if price.is_integer():
                price = int(price)
        except ValueError:
            price = 0

        yaml_lines.append(f'    qty: {qty}')
        yaml_lines.append(f'    unit_price_mxn: {price}')
        
        has_links = item.get("buy_amazon") or item.get("buy_aliexpress") or item.get("buy_other")
        if has_links:
            yaml_lines.append('    buy_links:')
            if item.get("buy_amazon"):
                yaml_lines.append(f'      amazon: "{item["buy_amazon"]}"')
            if item.get("buy_aliexpress"):
                yaml_lines.append(f'      aliexpress: "{item["buy_aliexpress"]}"')
            if item.get("buy_other"):
                yaml_lines.append(f'      other: "{item["buy_other"]}"')
    
    new_yaml_block = "\n".join(yaml_lines) + "\n"

    # Calcular costo total para actualizar en el yaml de manera opcional o mostrar
    total_cost = 0.0
    for item in bom_items:
        try:
            q = int(item.get("qty", 1))
            raw_price = item.get("unit_price_mxn") or item.get("unit_price_usd") or "0"
            p = float(raw_price)
            total_cost += q * p
        except ValueError:
            pass

    # 3. Generar Tabla Markdown para README.md
    md_lines = [
        "## 🛒 Bill of Materials",
        "",
        "| Qty | Componente | Descripción | Precio | Links |",
        "|-----|-----------|-------------|--------|-------|"
    ]
    for item in bom_items:
        qty = item.get("qty", "1")
        name = f'**{item["component"]}**'
        desc = item.get("description", "")
        raw_price = item.get("unit_price_mxn") or item.get("unit_price_usd") or "0"
        price = raw_price
        
        links = []
        if item.get("buy_amazon"):
            links.append(f'[Amazon]({item["buy_amazon"]})')
        if item.get("buy_aliexpress"):
            links.append(f'[AliExpress]({item["buy_aliexpress"]})')
        if item.get("buy_other"):
            links.append(f'[Otro]({item["buy_other"]})')
            
        links_str = " ".join(links) if links else "—"
        md_lines.append(f"| {qty} | {name} | {desc} | ${price} | {links_str} |")
    
    new_readme_block = "\n".join(md_lines) + "\n"

    # 4. Actualizar project.yml
    try:
        with open(project_yml_path, 'r', encoding='utf-8') as f:
            yml_content = f.read()

        # Reemplazar la sección bom:
        # Busca "bom:" al inicio de una línea y reemplaza hasta el próximo campo raíz (ej: "notes:") o final del archivo.
        pattern = r'^bom:.*?(?=^[a-z]+:|\Z)'
        updated_yml_content, count = re.subn(pattern, new_yaml_block, yml_content, flags=re.M | re.S)
        
        if count > 0:
            with open(project_yml_path, 'w', encoding='utf-8') as f:
                f.write(updated_yml_content)
            print("  [+] project.yml actualizado.")
        else:
            print("  [!] No se pudo encontrar la sección 'bom:' en project.yml.")
    except Exception as e:
        print(f"  [!] Error al actualizar project.yml: {e}")

    # 5. Actualizar README.md
    if os.path.exists(readme_path):
        try:
            with open(readme_path, 'r', encoding='utf-8') as f:
                readme_content = f.read()

            # Reemplazar la sección ## 🛒 Bill of Materials
            # Busca "## 🛒 Bill of Materials" hasta la siguiente sección de segundo nivel (ej: "## 🚀 Cómo empezar") o final.
            pattern_md = r'## 🛒 Bill of Materials.*?(?=## |\Z)'
            updated_readme_content, count_md = re.subn(pattern_md, new_readme_block, readme_content, flags=re.S)

            if count_md > 0:
                with open(readme_path, 'w', encoding='utf-8') as f:
                    f.write(updated_readme_content)
                print("  [+] README.md actualizado.")
            else:
                # Si no existía la sección, la añadimos antes de la sección "## 🚀 Cómo empezar"
                if "## 🚀 Cómo empezar" in readme_content:
                    readme_content = readme_content.replace("## 🚀 Cómo empezar", new_readme_block + "\n## 🚀 Cómo empezar")
                    with open(readme_path, 'w', encoding='utf-8') as f:
                        f.write(readme_content)
                    print("  [+] Sección BOM insertada en README.md.")
                else:
                    with open(readme_path, 'a', encoding='utf-8') as f:
                        f.write("\n" + new_readme_block)
                    print("  [+] Sección BOM añadida al final de README.md.")
        except Exception as e:
            print(f"  [!] Error al actualizar README.md: {e}")
            
    print(f"  [+] Costo estimado total de esta BOM: ${total_cost:.2f} MXN\n")
    return True

def main():
    # Determinar qué proyecto sincronizar
    target_dirs = []
    
    if len(sys.argv) > 1:
        # Se pasó un argumento
        path = sys.argv[1]
        if os.path.isdir(path):
            target_dirs.append(path)
        else:
            print(f"[-] El argumento proporcionado no es un directorio válido: {path}")
            sys.exit(1)
    else:
        # Sin argumentos: verificar directorio actual
        if os.path.exists('project.yml') and os.path.exists('assets/bom.csv'):
            target_dirs.append('.')
        else:
            # Buscar recursivamente en subdirectorios de primer y segundo nivel
            print("[*] Buscando proyectos con BOM en subdirectorios...")
            for root, dirs, files in os.walk('.'):
                # Ignorar carpetas ocultas y específicas
                dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ('docs', 'tests', 'assets', 'hmi', 'code', 'node_modules')]
                if 'project.yml' in files and os.path.exists(os.path.join(root, 'assets', 'bom.csv')):
                    target_dirs.append(root)

    if not target_dirs:
        print("[-] No se encontraron proyectos con 'project.yml' y 'assets/bom.csv' para sincronizar.")
        sys.exit(0)

    success_count = 0
    for d in target_dirs:
        if sync_project(d):
            success_count += 1

    print(f"[+] Sincronización finalizada. {success_count} proyecto(s) actualizados con éxito.")

if __name__ == '__main__':
    main()
