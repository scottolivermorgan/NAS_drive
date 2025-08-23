import yaml
import os

def load_config():
    """
    Load configuration from the main config.yml file.
    Falls back to config.example.yml if config.yml doesn't exist.
    
    Returns:
        dict: Configuration dictionary containing all settings
    """
    config_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'ansible')
    
    # Try to load config.yml first, then fall back to config.example.yml
    config_files = ['config.yml', 'config.example.yml']
    
    for config_file in config_files:
        config_path = os.path.join(config_dir, config_file)
        if os.path.exists(config_path):
            with open(config_path, 'r') as file:
                return yaml.safe_load(file)
    
    raise FileNotFoundError("No configuration file found (config.yml or config.example.yml)")

def get_server_config():
    """
    Get server configuration including IP addresses and all ports.
    
    Returns:
        dict: Server configuration with keys: server_ip, all individual ports as top-level keys
    """
    config = load_config()
    ports = config.get('ports', {})
    
    # Start with basic server config
    server_config = {
        'server_ip': config.get('server_ip', '192.168.2.179'),
        'ports': ports  # Keep the ports dict for structured access
    }
    
    # Add all ports as individual top-level keys for easy access
    for service, port in ports.items():
        server_config[f'{service}_port'] = port
    
    # Add legacy port variables for backward compatibility (only if not commented out)
    legacy_ntfy = config.get('ntfy_port')
    legacy_influxdb = config.get('influxdb_port')
    
    if legacy_ntfy is not None:
        server_config['ntfy_port'] = legacy_ntfy
    elif 'ntfy' in ports:
        server_config['ntfy_port'] = ports['ntfy']
    else:
        server_config['ntfy_port'] = 8090
        
    if legacy_influxdb is not None:
        server_config['influxdb_port'] = legacy_influxdb
    elif 'influxdb' in ports:
        server_config['influxdb_port'] = ports['influxdb']
    else:
        server_config['influxdb_port'] = 8086
    
    return server_config

def get_port(service_name, default_port=None):
    """
    Get port for a specific service.
    
    Args:
        service_name (str): Name of the service
        default_port (int): Default port if not found in config
    
    Returns:
        int: Port number for the service
    """
    config = load_config()
    ports = config.get('ports', {})
    
    # Try to get from ports section first
    if service_name in ports:
        return ports[service_name]
    
    # Fall back to legacy variables
    legacy_mapping = {
        'ntfy': config.get('ntfy_port', 8090),
        'influxdb': config.get('influxdb_port', 8086)
    }
    
    if service_name in legacy_mapping:
        return legacy_mapping[service_name]
    
    return default_port

def get_ntfy_url():
    """
    Get the complete ntfy notification URL.
    
    Returns:
        str: Complete ntfy base URL
    """
    server_config = get_server_config()
    ntfy_port = get_port('ntfy', 8090)  # Use the get_port function for consistency
    return f"http://{server_config['server_ip']}:{ntfy_port}"
