import graphviz

def create_vertical_structure():
    # Create a new directed graph
    dot = graphviz.Digraph(comment='Shopify App Store Structure')
    dot.attr(rankdir='TB')  # Top to bottom layout
    
    # Configure graph attributes for better layout
    dot.attr('graph', 
            nodesep='0.3',
            ranksep='0.6')
    
    # Set default node styles
    dot.attr('node', 
            shape='box',
            style='rounded,filled',
            fillcolor='white',
            fontsize='11',
            height='0.4',
            width='3.0')

    # Define the structure
    structure = {
        'navigation': {
            'label': 'Navigation & Search',
            'color': '#FFFFE0',
            'items': [
                'Global Search',
                'Category Navigation',
                'Search Filters',
                'User Account Menu'
            ]
        },
        'homepage': {
            'label': 'Homepage',
            'color': '#E0FFFF',
            'items': [
                'Featured Apps',
                'Trending Apps',
                'Category Showcase',
                'App Collections'
            ]
        },
        'categories': {
            'label': 'Category Pages',
            'color': '#FFB6C1',
            'items': [
                'Store Design & Themes',
                'Marketing & Conversion',
                'Orders & Shipping',
                'Sales Channels',
                'Finding Products',
                'Store Management'
            ]
        },
        'app_page': {
            'label': 'App Details Page',
            'color': '#98FB98',
            'items': [
                'App Overview & Screenshots',
                'Pricing & Installation',
                'Features & Benefits',
                'Reviews & Ratings',
                'Support & Documentation'
            ]
        }
    }

    # Create root node
    dot.node('root', 'Shopify App Store\napps.shopify.com', fillcolor='#ADD8E6', fontsize='14')

    # Add sections vertically
    prev_section = 'root'
    for section_id, section in structure.items():
        # Create section header
        header_id = f'{section_id}_header'
        dot.node(header_id, section['label'], fillcolor=section['color'], fontsize='12')
        dot.edge(prev_section, header_id)
        
        # Create items in the section
        with dot.subgraph(name=f'cluster_{section_id}') as c:
            c.attr(style='rounded', color=section['color'])
            for i, item in enumerate(section['items']):
                item_id = f'{section_id}_item_{i}'
                c.node(item_id, item, fillcolor=section['color'])
                dot.edge(header_id, item_id)
        
        prev_section = header_id

    return dot

def main():
    # Create visualization
    dot = create_vertical_structure()
    
    # Save with vertical dimensions
    dot.attr(size='8,16!')  # Taller than wide
    dot.render('shopify_appstore_vertical', format='png', cleanup=True)
    print("Vertical App Store structure visualization saved as 'shopify_appstore_vertical.png'")
    
    # Save as SVG for better quality
    dot.render('shopify_appstore_vertical', format='svg', cleanup=True)
    print("Vertical App Store structure visualization saved as 'shopify_appstore_vertical.svg'")

if __name__ == "__main__":
    main() 