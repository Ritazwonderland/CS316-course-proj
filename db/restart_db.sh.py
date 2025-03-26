import subprocess
import time

def get_postgres_pids():
    try:
        # Get all postgres processes for amazon database
        cmd = """psql -d amazon -c "SELECT pid FROM pg_stat_activity WHERE datname = 'amazon';" """
        result = subprocess.check_output(cmd, shell=True).decode()
        
        # Parse PIDs from the output
        lines = result.strip().split('\n')
        pids = []
        for line in lines[2:-1]:  # Skip header and footer lines
            if line.strip():
                pids.append(line.strip())
        return pids
    except:
        return []

def main():
    print("🔄 Restarting database...")
    
    # Get all postgres processes
    pids = get_postgres_pids()
    
    if not pids:
        print("No active postgres connections found")
    else:
        print(f"Found {len(pids)} active connections")
        
        # Terminate each process
        for pid in pids:
            try:
                cmd = f"""psql -d amazon -c "SELECT pg_terminate_backend({pid});" """
                subprocess.run(cmd, shell=True, check=True)
                print(f"✓ Terminated process {pid}")
            except subprocess.CalledProcessError:
                print(f"✗ Failed to terminate process {pid}")
    
    # Small delay to ensure all connections are closed
    time.sleep(1)
    
    # Run setup script
    print("\n🔄 Running database setup script...")
    try:
        subprocess.run("./db/setup.sh", shell=True, check=True)
        print("✅ Database reset successfully!")
    except subprocess.CalledProcessError:
        print("❌ Failed to reset database")

if __name__ == "__main__":
    main() 