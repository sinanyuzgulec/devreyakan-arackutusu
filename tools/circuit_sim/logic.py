
import numpy as np
import core.localization as loc
class CircuitSolver:
    def __init__(self):
        self.nodes = set()
        self.components = []
        self.node_map = {}  
        
    def parse_netlist(self, netlist_text):
       
        self.components = []
        self.nodes = set(['0']) 
        
        lines = netlist_text.strip().split('\n')
        for line in lines:
            line = line.strip()
            if not line or line.startswith('*'): continue
            
            parts = line.split()
            if len(parts) < 4: continue
            
            type_char = parts[0][0].upper()
            name = parts[0]
            n1 = parts[1]
            n2 = parts[2]
            
            
            val_str = parts[3].lower().replace('k', 'e3').replace('m', 'e-3').replace('u', 'e-6')
            try:
                value = float(val_str)
            except:
                continue

            self.nodes.add(n1)
            self.nodes.add(n2)
            
            self.components.append({
                'type': type_char,
                'name': name,
                'n1': n1,
                'n2': n2,
                'value': value
            })

    def solve(self):
        
        
        
        
        sorted_nodes = sorted(list(self.nodes))
        if '0' in sorted_nodes: sorted_nodes.remove('0')
        
        node_count = len(sorted_nodes)
        self.node_map = {n: i for i, n in enumerate(sorted_nodes)}
        
        
        v_sources = [c for c in self.components if c['type'] == 'V']
        m_count = len(v_sources)
        
        total_dim = node_count + m_count
        
        
        G = np.zeros((total_dim, total_dim))
        I = np.zeros(total_dim)
        
        
        for comp in self.components:
            n1 = comp['n1']
            n2 = comp['n2']
            val = comp['value']
            
            idx1 = self.node_map.get(n1)
            idx2 = self.node_map.get(n2)
            
            if comp['type'] == 'R':
                g = 1.0 / val
                if idx1 is not None:
                    G[idx1, idx1] += g
                    if idx2 is not None: G[idx1, idx2] -= g
                if idx2 is not None:
                    G[idx2, idx2] += g
                    if idx1 is not None: G[idx2, idx1] -= g
                    
            elif comp['type'] == 'I':
                
                if idx1 is not None: I[idx1] -= val
                if idx2 is not None: I[idx2] += val

        
        
        for i, v_src in enumerate(v_sources):
            idx_v = node_count + i 
            
            n1 = v_src['n1']
            n2 = v_src['n2']
            val = v_src['value']
            
            idx1 = self.node_map.get(n1)
            idx2 = self.node_map.get(n2)
            
            
            if idx1 is not None:
                G[idx1, idx_v] = 1
                G[idx_v, idx1] = 1
            
            if idx2 is not None:
                G[idx2, idx_v] = -1
                G[idx_v, idx2] = -1
                
            
            I[idx_v] = val

        
        try:
            x = np.linalg.solve(G, I)
        except np.linalg.LinAlgError:
            return None, loc.get("circuit_sim_solution_failed")

        
        results = {}
        
        for node, idx in self.node_map.items():
            results[f"V({node})"] = x[idx]
            
        
        for i, v_src in enumerate(v_sources):
            idx_v = node_count + i
            
            results[f"I({v_src['name']})"] = -x[idx_v]
            
        return results, loc.get("circuit_sim_solution_successful")