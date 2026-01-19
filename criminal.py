import pandas as pd
import networkx as nx
import json
from networkx.algorithms import community

# --- CONFIGURATION DU LOGO ---
# Utilisation du fichier local nommé Logo.png
LOGO_URL = "Logo.png"
# -----------------------------

def generate_landing_page():
    """Génère la page d'accueil index.html avec le logo et favicon"""
    html = f"""
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>PrisonLink - Accueil</title>
    
    <!-- Favicon -->
    <link rel="icon" type="image/png" href="{LOGO_URL}">
    
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;700;800&display=swap" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
    <style>
        :root {{
            --primary: #0d6efd;
            --text: #212529;
            --bg: #f8f9fa;
        }}
        body {{
            margin: 0; padding: 0;
            font-family: 'Outfit', sans-serif;
            background-color: var(--bg);
            color: var(--text);
            height: 100vh;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            background-image: radial-gradient(#adb5bd 1px, transparent 1px);
            background-size: 30px 30px;
            overflow: hidden;
        }}
        .container {{
            text-align: center;
            background: rgba(255, 255, 255, 0.9);
            padding: 60px;
            border-radius: 24px;
            box-shadow: 0 20px 50px rgba(0,0,0,0.1);
            border: 1px solid #fff;
            max-width: 600px;
            position: relative;
            animation: slideUp 0.8s cubic-bezier(0.2, 0.8, 0.2, 1);
        }}
        
        /* Logo style */
        .logo-main {{
            width: 150px;
            height: 150px;
            object-fit: contain;
            margin-bottom: 20px;
            filter: drop-shadow(0 10px 15px rgba(0,0,0,0.1));
            border-radius: 20px;
        }}

        h1 {{
            font-size: 4rem;
            font-weight: 800;
            margin: 0;
            background: linear-gradient(135deg, #0d6efd, #0a58ca);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            letter-spacing: -2px;
        }}
        .subtitle {{
            font-size: 1.2rem;
            color: #6c757d;
            margin-top: 10px;
            margin-bottom: 30px;
            font-weight: 400;
            text-transform: uppercase;
            letter-spacing: 2px;
        }}
        .description {{
            font-size: 1.1rem;
            color: #495057;
            line-height: 1.6;
            margin-bottom: 40px;
        }}
        .btn {{
            display: inline-block;
            padding: 18px 40px;
            font-size: 1.2rem;
            font-weight: 700;
            color: #fff;
            background: var(--primary);
            border-radius: 50px;
            text-decoration: none;
            transition: all 0.3s ease;
            box-shadow: 0 10px 25px rgba(13, 110, 253, 0.3);
        }}
        .btn:hover {{
            transform: translateY(-5px);
            box-shadow: 0 15px 35px rgba(13, 110, 253, 0.4);
            background: #0b5ed7;
        }}
        
        .icon {{ font-size: 3rem; color: var(--primary); margin-bottom: 20px; }}
        
        @keyframes slideUp {{
            from {{ opacity: 0; transform: translateY(40px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}
        
        /* Floating decoration */
        .circle {{
            position: absolute;
            border-radius: 50%;
            background: var(--primary);
            opacity: 0.1;
            z-index: -1;
        }}
        .c1 {{ width: 300px; height: 300px; top: -100px; left: -100px; }}
        .c2 {{ width: 200px; height: 200px; bottom: -50px; right: -50px; background: #fd7e14; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="circle c1"></div>
        <div class="circle c2"></div>
        
        <!-- Intégration du logo local Logo.png -->
        <img src="{LOGO_URL}" alt="Prison Nexus Logo" class="logo-main">
        
        <h1>PrisonLink</h1>
        <div class="subtitle">Intelligence Pénitentiaire</div>
        
        <p class="description">
            Explorez les connexions cachées au sein du système carcéral. 
            Notre algorithme analyse les périodes de co-incarcération pour révéler 
            les réseaux d'influence et les interactions entre détenus.
        </p>
        
        <a href="prison_dashboard.html" class="btn">
            Accéder au Dashboard <i class="fas fa-arrow-right" style="margin-left: 10px;"></i>
        </a>
    </div>
</body>
</html>
    """
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("Page d'accueil 'index.html' générée.")

def generate_dashboard():
    # --- CONFIGURATION ---
    MIN_DURATION_FILTER = 24 
    # ---------------------

    print(f"Chargement des données... (Base: > {MIN_DURATION_FILTER}h ensemble)")
    try:
        # 1. Chargement et nettoyage
        try:
            df = pd.read_csv('données nettoyés.csv', sep=';', encoding='utf-8')
        except UnicodeDecodeError:
            print("Encodage UTF-8 échoué, passage en Latin-1...")
            df = pd.read_csv('données nettoyés.csv', sep=';', encoding='latin-1')
        
        df['Full Name'] = df['First Name'].str.strip() + ' ' + df['Last Name'].str.strip()
        
        date_format = "%Y %b %d %I:%M:%S %p"
        df['Booking Date Time'] = pd.to_datetime(df['Booking Date Time'], format=date_format, errors='coerce')
        df['Release Date Time'] = pd.to_datetime(df['Release Date Time'], format=date_format, errors='coerce')
        
        df = df.dropna(subset=['Booking Date Time', 'Release Date Time', 'Full Name'])

        # 2. Extraction des charges
        person_charges = {}
        for index, row in df.iterrows():
            name = row['Full Name']
            charge = str(row['Charge']).strip()
            if name not in person_charges:
                person_charges[name] = set()
            if charge and charge.lower() != 'nan':
                person_charges[name].add(charge)

        # 3. Consolidation des séjours
        stays = df.groupby(['Book of Arrest Number', 'Full Name', 'Current Facility']).agg({
            'Booking Date Time': 'min',
            'Release Date Time': 'max'
        }).reset_index()

        print(f"{len(stays)} séjours identifiés. Calcul des interactions...")

        # 4. Calcul des paires et suivi des établissements
        potential_edges = []
        facilities = stays['Current Facility'].unique()
        person_facilities = {} 
        
        for facility in facilities:
            facility_stays = stays[stays['Current Facility'] == facility].to_dict('records')
            n = len(facility_stays)
            
            for p in facility_stays:
                name = p['Full Name']
                if name not in person_facilities:
                    person_facilities[name] = set()
                person_facilities[name].add(facility)

            for i in range(n):
                for j in range(i + 1, n):
                    p1 = facility_stays[i]
                    p2 = facility_stays[j]
                    
                    if p1['Full Name'] == p2['Full Name']:
                        continue
                    
                    start_overlap = max(p1['Booking Date Time'], p2['Booking Date Time'])
                    end_overlap = min(p1['Release Date Time'], p2['Release Date Time'])
                    
                    if end_overlap > start_overlap:
                        duration_hours = (end_overlap - start_overlap).total_seconds() / 3600
                        
                        if duration_hours >= MIN_DURATION_FILTER:
                            potential_edges.append({
                                'source': p1['Full Name'],
                                'target': p2['Full Name'],
                                'weight': duration_hours
                            })

        # 5. Agrégation
        edges_map = {}
        for edge in potential_edges:
            key = tuple(sorted((edge['source'], edge['target'])))
            if key in edges_map:
                edges_map[key] += edge['weight']
            else:
                edges_map[key] = edge['weight']
        
        final_edges = [(k, v) for k, v in edges_map.items()]
        final_edges.sort(key=lambda x: x[1], reverse=True)
        
        print(f"Relations conservées: {len(final_edges)}.")

        # 6. Construction du Graphe
        G = nx.Graph()
        for (source, target), duration in final_edges:
            G.add_edge(source, target, weight=duration)

        # 6bis. CALCUL CENTRALITÉ (Influence)
        print("Calcul de la centralité (Influence)...")
        centrality = nx.betweenness_centrality(G, weight='weight')

        # 7. Données Visuelles avec GROUPES par Etablissement
        print("Génération du design...")
        node_data = []
        for person in G.nodes():
            degree = G.degree[person]
            score = centrality.get(person, 0)
            
            p_facilities = list(person_facilities.get(person, []))
            p_charges = list(person_charges.get(person, []))
            
            charges_display = ", ".join(p_charges[:3])
            if len(p_charges) > 3: charges_display += ", ..."

            main_facility = p_facilities[0] if p_facilities else "Inconnu"

            node_data.append({
                "id": person, 
                "label": person, 
                "group": main_facility, 
                "value": degree, 
                "influence": score,
                "facilities": p_facilities, 
                "charges": p_charges,
                "title": f"{person}\nConnexions: {degree}\nInfluence: {score:.4f}\nCharges: {charges_display}"
            })

        edge_data = []
        max_duration = final_edges[0][1] if final_edges else 1
        
        for u, v, data in G.edges(data=True):
            duration = data['weight']
            days = duration / 24
            width = 1 + (duration / max_duration) * 6
            
            edge_data.append({
                "from": u, 
                "to": v,
                "width": width,
                "title": f"{days:.1f} jours ensemble", 
                "days_count": f"{days:.1f}",
                "raw_days": float(f"{days:.2f}"),
                "color": { "color": "rgba(100, 100, 100, 0.2)", "highlight": "#000000" } 
            })
        
        all_facilities_list = sorted(list(facilities))
        
        network_data = {
            "nodes": node_data,
            "edges": edge_data,
            "facilities": all_facilities_list
        }
        
        # --- EXPORT JSON ---
        with open('network_data.json', 'w', encoding='utf-8') as f:
            json.dump(network_data, f, ensure_ascii=False, indent=4)
        
        json_str = json.dumps(network_data)

        # 8. HTML & CSS
        html_content = f"""
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Analyse Réseau - Dashboard</title>
    
    <!-- Favicon -->
    <link rel="icon" type="image/png" href="{LOGO_URL}">
    
    <script type="text/javascript" src="https://unpkg.com/vis-network/standalone/umd/vis-network.min.js"></script>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
    
    <style>
        :root {{
            --text: #212529;
            --background: #f8f9fa;
            --primary: #0d6efd; 
            --secondary: #fd7e14;
            --accent: #198754; 
            
            --panel-bg: rgba(255, 255, 255, 0.95);
            --shadow: 0 4px 12px rgba(0,0,0,0.15);
            --border: 1px solid #dee2e6;
        }}

        body {{ 
            margin: 0; padding: 0; background-color: var(--background); color: var(--text); 
            font-family: 'Outfit', sans-serif; overflow: hidden; 
            background-image: radial-gradient(#adb5bd 1px, transparent 1px);
            background-size: 30px 30px;
        }}
        
        #mynetwork {{ width: 100vw; height: 100vh; position: absolute; top:0; left:0; z-index: 1; outline: none; }}

        .sidebar {{ 
            position: absolute; top: 20px; left: 20px; width: 340px; z-index: 10;
            background: var(--panel-bg); backdrop-filter: blur(10px); -webkit-backdrop-filter: blur(10px);
            border-radius: 12px; box-shadow: var(--shadow); padding: 25px;
            max-height: 90vh; overflow-y: auto; border: var(--border);
        }}
        
        .sidebar-header {{
            display: flex; align-items: center; gap: 12px; margin-bottom: 25px;
        }}
        
        .logo-sidebar {{
            width: 45px; height: 45px; object-fit: contain; border-radius: 8px;
        }}

        h1 {{ font-weight: 700; font-size: 22px; margin: 0; color: var(--primary); display: flex; align-items: center; gap: 12px; }}
        .section-title {{ font-size: 11px; font-weight: 700; text-transform: uppercase; color: #6c757d; margin-bottom: 12px; margin-top: 25px; letter-spacing: 1px; display: flex; justify-content: space-between; align-items: center; }}

        .input-wrapper {{ position: relative; margin-bottom:10px; }}
        input[type="text"], select {{
            width: 100%; padding: 12px 15px; padding-left: 40px;
            background: #fff; border: 1px solid #ced4da;
            border-radius: 8px; color: var(--text); font-family: 'Outfit', sans-serif;
            transition: all 0.2s ease; box-sizing: border-box; font-size: 14px;
        }}
        select {{ padding-left: 15px; cursor: pointer; }}
        input[type="text"]:focus, select:focus {{ outline: none; border-color: var(--primary); box-shadow: 0 0 0 3px rgba(13, 110, 253, 0.25); }}
        .search-icon {{ position: absolute; left: 14px; top: 13px; color: var(--primary); pointer-events: none; }}

        .slider-box {{ padding: 15px; background: #fff; border-radius: 8px; border: 1px solid #ced4da; margin-bottom: 10px; }}
        .slider-header {{ display: flex; justify_content: space-between; font-size: 13px; color: #495057; margin-bottom: 10px; font-weight: 500; }}
        .slider-value {{ color: #fff; font-weight: 700; background: var(--primary); padding: 2px 8px; border-radius: 6px; font-size: 11px; }}
        
        input[type="range"] {{ width: 100%; cursor: pointer; accent-color: var(--primary); height: 5px; background: #e9ecef; border-radius: 3px; appearance: none; }}
        
        .info-card {{
            display: none; margin-top: 25px; background: #fff; border-radius: 12px;
            box-shadow: var(--shadow); padding: 20px; position: relative; overflow: hidden;
            animation: slideUp 0.4s cubic-bezier(0.16, 1, 0.3, 1); border: 1px solid #dee2e6;
        }}
        .info-card::before {{ content: ''; position: absolute; top:0; left:0; width: 6px; height: 100%; background: var(--secondary); }}
        .info-card.active {{ display: block; }}
        
        .info-title {{ font-size: 18px; font-weight: 700; margin-bottom: 15px; color: var(--text); border-bottom: 1px solid #eee; padding-bottom: 10px; }}
        .info-row {{ display: flex; justify_content: space-between; font-size: 13px; margin-bottom: 8px; }}
        .info-label {{ color: #6c757d; font-weight: 500; }}
        .info-val {{ color: var(--text); font-weight: 600; text-align: right; max-width: 60%; }}

        .tag-container {{ display: flex; flex-wrap: wrap; gap: 5px; margin-top: 10px; }}
        .tag {{ background: #e9ecef; color: #495057; font-size: 10px; padding: 3px 8px; border-radius: 4px; font-weight: 600; }}

        .stats-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin-bottom: 10px; }}
        .stat-box {{ background: #fff; padding: 15px; border-radius: 12px; text-align: center; border: 1px solid #ced4da; }}
        .stat-num {{ font-size: 24px; font-weight: 700; color: var(--primary); display: block; line-height: 1; }}
        .stat-desc {{ font-size: 10px; color: #6c757d; text-transform: uppercase; font-weight: 600; }}

        .top-box {{ background: #fff; padding: 10px; border-radius: 12px; border: 1px solid #ced4da; margin-bottom: 20px; }}
        .top-item {{ display: flex; justify_content: space-between; align-items: center; padding: 8px; border-bottom: 1px solid #eee; font-size: 13px; cursor: pointer; transition: 0.2s; }}
        .top-item:last-child {{ border-bottom: none; }}
        .top-item:hover {{ background: #f8f9fa; color: var(--primary); }}
        .top-rank {{ font-weight: 700; color: var(--secondary); margin-right: 10px; width: 15px; }}
        .top-name {{ flex-grow: 1; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }}
        .top-score {{ font-size: 10px; color: #adb5bd; }}

        .btn-group {{ display: flex; gap: 10px; margin-top: 20px; }}
        .btn {{ flex: 1; padding: 12px; background: var(--primary); color: #fff; border: none; border-radius: 8px; cursor: pointer; font-weight: 600; font-size: 13px; transition: all 0.2s; display: flex; justify-content: center; align-items: center; gap: 8px; }}
        .btn:hover {{ background: #0b5ed7; transform: translateY(-2px); }}
        .btn-secondary {{ background: #fff; color: #495057; border: 1px solid #ced4da; }}
        .btn-secondary:hover {{ background: #f8f9fa; color: #212529; }}

        #loading-screen {{ position: fixed; inset: 0; background: var(--background); z-index: 100; display: flex; flex-direction: column; align-items: center; justify-content: center; transition: opacity 0.5s; }}
        .logo-loading {{ width: 100px; margin-bottom: 20px; }}
        .spinner {{ width: 50px; height: 50px; border: 4px solid #dee2e6; border-top: 4px solid var(--primary); border-radius: 50%; animation: spin 0.8s infinite; margin-bottom: 20px; }}
        @keyframes spin {{ 0% {{ transform: rotate(0deg); }} 100% {{ transform: rotate(360deg); }} }}
        @keyframes slideUp {{ from {{ opacity: 0; transform: translateY(20px); }} to {{ opacity: 1; transform: translateY(0); }} }}
    </style>
</head>
<body>

    <div id="loading-screen">
        <img src="{LOGO_URL}" class="logo-loading" alt="Logo">
        <div class="spinner"></div>
        <div style="font-size: 14px; font-weight: 600; color: var(--primary); letter-spacing: 2px;">CHARGEMENT DU SYSTÈME</div>
    </div>

    <div id="mynetwork"></div>

    <div class="sidebar">
        <div class="sidebar-header">
            <img src="{LOGO_URL}" alt="Logo" class="logo-sidebar">
            <h1>Network Intel.</h1>
        </div>
        
        <div class="stats-grid">
            <div class="stat-box">
                <span class="stat-num" id="stat-nodes">0</span>
                <span class="stat-desc">Détenus</span>
            </div>
            <div class="stat-box">
                <span class="stat-num" id="stat-edges">0</span>
                <span class="stat-desc">Connexions</span>
            </div>
        </div>

        <div class="section-title"><span>Top Influenceurs</span> <i class="fas fa-crown" style="color:var(--secondary)"></i></div>
        <div class="top-box" id="top-list">
            <!-- Rempli par JS -->
        </div>
        
        <div class="section-title"><span>Filtres Globaux</span> <i class="fas fa-sliders-h"></i></div>
        
        <div class="input-wrapper">
             <select id="facility-select">
                <option value="all">🏢 Tous les établissements</option>
             </select>
        </div>

        <div class="slider-box">
            <div class="slider-header"><span><i class="fas fa-clock"></i> Durée min.</span><span class="slider-value" id="days-display">1j</span></div>
            <input type="range" id="daysFilter" min="1" max="100" value="1" step="1">
        </div>

        <div class="slider-box">
            <div class="slider-header"><span><i class="fas fa-users"></i> Importance</span><span class="slider-value" id="degree-display">0+</span></div>
            <input type="range" id="degreeFilter" min="0" max="20" value="0" step="1">
        </div>
        
        <div class="section-title"><span>Recherche</span> <i class="fas fa-search"></i></div>
        <div class="input-wrapper">
            <i class="fas fa-search search-icon"></i>
            <input type="text" id="search-input" list="names" placeholder="Nom ou Charge...">
            <datalist id="names"></datalist>
        </div>

        <div id="info-card" class="info-card">
            <div class="info-title" id="info-title">Nom</div>
            <div class="info-row"><span class="info-label">Etablissement</span> <span class="info-val" id="info-fac">-</span></div>
            <div class="info-row"><span class="info-label">Connexions</span> <span class="info-val" id="info-conns">-</span></div>
            <div class="info-row"><span class="info-label">Influence</span> <span class="info-val" id="info-score">-</span></div>
            <div class="info-row" id="row-duration" style="display:none"><span class="info-label">Durée</span> <span class="info-val" id="info-duration">-</span></div>
            <div id="charges-container" style="display:none; margin-top:10px; border-top:1px solid #dee2e6; padding-top:10px;">
                <span class="info-label" style="font-size:11px;">CHARGES</span>
                <div class="tag-container" id="charges-tags"></div>
            </div>
        </div>

        <div class="btn-group">
            <button class="btn" onclick="exportCanvas()"><i class="fas fa-camera"></i> Photo</button>
            <button class="btn btn-secondary" onclick="togglePhysics()" id="btn-physics"><i class="fas fa-pause"></i> Pause</button>
        </div>
        
        <div style="margin-top: 15px; text-align:center;">
             <button class="btn btn-secondary" style="width:100%" onclick="resetView()"><i class="fas fa-sync-alt"></i> Reset Vue</button>
        </div>
        
        <div style="margin-top: 20px; font-size: 11px; text-align: center;">
            <a href="index.html" style="color: var(--primary); text-decoration: none;">Retour Accueil</a>
        </div>
    </div>

    <script>
        const rawData = {json_str};
        
        const theme = {{
            primary: '#0d6efd',   // Bleu Franc
            secondary: '#fd7e14', // Orange Franc
            accent: '#198754',    // Vert Franc
            text: '#212529'
        }};

        // DataSets
        const allEdges = rawData.edges;
        const allNodes = rawData.nodes;
        const nodes = new vis.DataSet(allNodes);
        const edges = new vis.DataSet(allEdges);
        const container = document.getElementById('mynetwork');
        
        // --- COULEURS PAR ETABLISSEMENT (SIMPLE & VISIBLE) ---
        const groupsConfig = {{
            'King County Correctional Facility': {{ 
                color: {{ background: theme.primary, border: '#0a58ca', highlight: {{ background: '#0b5ed7', border: '#0a58ca' }} }},
                font: {{ color: '#fff' }}
            }},
            'Maleng Regional Justice Center': {{ 
                color: {{ background: theme.accent, border: '#146c43', highlight: {{ background: '#157347', border: '#146c43' }} }},
                font: {{ color: '#fff' }}
            }},
            'Electronic Home Detention': {{ 
                color: {{ background: theme.secondary, border: '#e65c00', highlight: {{ background: '#e65c00', border: '#e65c00' }} }},
                font: {{ color: '#fff' }}
            }},
            'Inconnu': {{
                color: {{ background: '#6c757d', border: '#495057' }},
                font: {{ color: '#fff' }}
            }},
            'default': {{
                color: {{ background: '#adb5bd', border: '#6c757d' }}
            }}
        }};

        const options = {{
            groups: groupsConfig,
            nodes: {{
                shape: 'dot', size: 14, borderWidth: 2,
                font: {{ size: 14, color: theme.text, face: 'Outfit', strokeWidth: 3, strokeColor: '#ffffff' }},
                shadow: {{ enabled: true, color: 'rgba(0,0,0,0.2)', size: 10, x: 0, y: 5 }}
            }},
            edges: {{
                smooth: {{ type: 'continuous', roundness: 0.5 }},
                color: {{ color: 'rgba(100, 100, 100, 0.2)', highlight: theme.primary, hover: theme.primary }},
                width: 1
            }},
            physics: {{
                forceAtlas2Based: {{ gravitationalConstant: -60, centralGravity: 0.008, springLength: 120, springConstant: 0.06, damping: 0.9, avoidOverlap: 0.5 }},
                maxVelocity: 5, minVelocity: 0.1, timestep: 0.2, adaptiveTimestep: true,
                solver: 'forceAtlas2Based', stabilization: {{ enabled: true, iterations: 1000 }}
            }},
            interaction: {{ hover: true, tooltipDelay: 200, hideEdgesOnDrag: true, zoomView: true }}
        }};

        const network = new vis.Network(container, {{nodes, edges}}, options);

        network.on("stabilizationIterationsDone", function () {{
            document.getElementById('loading-screen').style.opacity = '0';
            setTimeout(() => {{ document.getElementById('loading-screen').style.display = 'none'; }}, 500);
        }});

        // --- GLOBAL STATE ---
        let currentFocusId = null;

        // DOM
        const daysSlider = document.getElementById('daysFilter');
        const degreeSlider = document.getElementById('degreeFilter');
        const facSelect = document.getElementById('facility-select');
        const statEdges = document.getElementById('stat-edges');
        const statNodes = document.getElementById('stat-nodes');
        const topList = document.getElementById('top-list');

        // Init Stats
        statNodes.innerText = allNodes.length;
        statEdges.innerText = allEdges.length;

        // --- POPULATE TOP 5 INFLUENCEURS ---
        const sortedByInfluence = [...rawData.nodes].sort((a,b) => (b.influence || 0) - (a.influence || 0));
        const top5 = sortedByInfluence.slice(0, 5);
        
        top5.forEach((n, index) => {{
            const div = document.createElement('div');
            div.className = 'top-item';
            div.innerHTML = `<span class="top-rank">#${{index+1}}</span> <span class="top-name">${{n.label}}</span> <span class="top-score">${{(n.influence*100).toFixed(1)}}</span>`;
            div.onclick = () => focusNode(n.id);
            topList.appendChild(div);
        }});

        // Populate Lists
        const dataList = document.getElementById('names');
        rawData.nodes.sort((a,b) => a.label.localeCompare(b.label)).forEach(n => {{
            const opt = document.createElement('option');
            opt.value = n.label; dataList.appendChild(opt);
        }});
        
        let allCharges = new Set();
        rawData.nodes.forEach(n => n.charges.forEach(c => allCharges.add(c)));
        Array.from(allCharges).sort().forEach(c => {{
            const opt = document.createElement('option');
            opt.value = c; opt.innerText = "Charge: " + c; dataList.appendChild(opt);
        }});

        if (rawData.facilities) {{
            rawData.facilities.forEach(fac => {{
                const opt = document.createElement('option');
                opt.value = fac; opt.innerText = "🏢 " + fac; facSelect.appendChild(opt);
            }});
        }}

        // --- CŒUR DU SYSTÈME : VISIBILITÉ CENTRALISÉE ---
        function updateVisibility() {{
            const minDays = parseInt(daysSlider.value);
            const minDegree = parseInt(degreeSlider.value);
            const selectedFac = facSelect.value;
            
            document.getElementById('days-display').innerText = minDays + "j";
            document.getElementById('degree-display').innerText = minDegree + "+";

            let focusSet = null;
            if (currentFocusId !== null) {{
                focusSet = new Set();
                focusSet.add(currentFocusId);
                allEdges.forEach(e => {{
                    if (e.raw_days >= minDays) {{
                        if (e.from === currentFocusId) focusSet.add(e.to);
                        if (e.to === currentFocusId) focusSet.add(e.from);
                    }}
                }});
            }}

            const nodesUpdates = [];
            let visibleNodeIds = new Set();

            nodes.forEach(n => {{
                const matchFac = (selectedFac === 'all') || (n.facilities && n.facilities.includes(selectedFac));
                const matchDegree = n.value >= minDegree;
                const matchesGlobal = matchFac && matchDegree;
                const matchesFocus = (focusSet === null) || focusSet.has(n.id);
                const shouldShow = matchesGlobal && matchesFocus;

                if (shouldShow) {{
                    visibleNodeIds.add(n.id);
                    if (n.hidden === true) nodesUpdates.push({{id: n.id, hidden: false}});
                }} else {{
                    if (n.hidden !== true) nodesUpdates.push({{id: n.id, hidden: true}});
                }}
            }});
            nodes.update(nodesUpdates);

            const filteredEdges = allEdges.filter(e => {{
                if (e.raw_days < minDays) return false;
                if (!visibleNodeIds.has(e.from) || !visibleNodeIds.has(e.to)) return false;
                return true;
            }});

            edges.clear();
            edges.add(filteredEdges);

            statNodes.innerText = visibleNodeIds.size;
            statEdges.innerText = filteredEdges.length;
        }}

        daysSlider.addEventListener('input', updateVisibility);
        degreeSlider.addEventListener('input', updateVisibility);
        facSelect.addEventListener('change', updateVisibility);

        // --- ACTIONS ---
        function focusNode(id) {{
            currentFocusId = id; 
            updateVisibility();
            network.focus(id, {{ scale: 1.0, animation: {{ duration: 800, easingFunction: 'easeInOutQuad' }} }});
            network.selectNodes([id]);
            const node = nodes.get(id);
            const connectedCount = network.getConnectedNodes(id).length;
            let facDisplay = node.facilities && node.facilities.length ? node.facilities[0] : "-";
            if (node.facilities && node.facilities.length > 1) facDisplay += " (+)";
            showInfo(node, facDisplay, connectedCount, null);
        }}

        function resetView() {{
            currentFocusId = null;
            updateVisibility();
            network.fit({{ animation: {{ duration: 1000 }} }});
            document.getElementById('search-input').value = '';
            document.getElementById('info-card').classList.remove('active');
        }}

        // --- EXPORT PHOTO ---
        function exportCanvas() {{
            const canvas = document.querySelector('canvas');
            const link = document.createElement('a');
            link.download = 'prison_network_evidence.png';
            link.href = canvas.toDataURL();
            link.click();
        }}

        // --- RECHERCHE ---
        document.getElementById('search-input').addEventListener('change', function() {{
            const val = this.value.toLowerCase();
            let found = nodes.get({{filter: item => item.label.toLowerCase() === val}});
            
            if (found.length === 0) {{
                const matchedIds = [];
                nodes.forEach(n => {{
                    if (n.charges && n.charges.some(c => c.toLowerCase().includes(val))) matchedIds.push(n.id);
                }});
                if (matchedIds.length > 0) focusNode(matchedIds[0]);
            }} else {{
                focusNode(found[0].id);
            }}
        }});

        network.on("click", function(params) {{
            if (params.nodes.length > 0) {{
                focusNode(params.nodes[0]);
            }} else if (params.edges.length > 0) {{
                const edge = edges.get(params.edges[0]);
                showInfo(null, null, null, edge.days_count + " jours");
            }} else {{
                document.getElementById('info-card').classList.remove('active');
            }}
        }});

        function showInfo(data, fac, conns, duration) {{
            const card = document.getElementById('info-card');
            const chargesContainer = document.getElementById('charges-container');
            const chargesTags = document.getElementById('charges-tags');
            
            if(duration) {{
                document.getElementById('info-title').innerText = "Relation";
                document.getElementById('info-fac').innerText = "-";
                document.getElementById('info-conns').innerText = "-";
                document.getElementById('info-score').innerText = "-";
                document.getElementById('row-duration').style.display = 'flex';
                document.getElementById('info-duration').innerText = duration;
                chargesContainer.style.display = 'none';
            }} else {{
                document.getElementById('info-title').innerText = data.label;
                document.getElementById('info-fac').innerText = fac;
                document.getElementById('info-conns').innerText = conns;
                document.getElementById('info-score').innerText = (data.influence * 100).toFixed(2);
                document.getElementById('row-duration').style.display = 'none';
                
                chargesTags.innerHTML = '';
                if(data.charges && data.charges.length > 0) {{
                    chargesContainer.style.display = 'block';
                    data.charges.forEach(c => {{
                        const tag = document.createElement('div');
                        tag.className = 'tag'; tag.innerText = c; chargesTags.appendChild(tag);
                    }});
                }} else {{ chargesContainer.style.display = 'none'; }}
            }}
            card.classList.add('active');
        }}

        let physicsOn = true;
        function togglePhysics() {{
            physicsOn = !physicsOn;
            network.setOptions({{physics: physicsOn}});
            const btn = document.getElementById('btn-physics');
            btn.innerHTML = physicsOn ? '<i class="fas fa-pause"></i> Pause' : '<i class="fas fa-play"></i> Play';
        }}
        
        updateVisibility();
    </script>
</body>
</html>
        """
        
        output_file = "prison_dashboard.html"
        with open(output_file, "w", encoding='utf-8') as f:
            f.write(html_content)
        print(f"Interface Moderne générée : '{output_file}'")

    except Exception as e:
        print(f"Erreur critique: {e}")

    generate_landing_page()

if __name__ == "__main__":
    generate_dashboard()
