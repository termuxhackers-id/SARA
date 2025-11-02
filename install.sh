#!/bin/bash
# SARA v3.1 - Auto Installation Script
# Supports: Termux & Linux (Debian/Ubuntu/Arch)

# Colors
RED='\033[1;91m'
GREEN='\033[1;92m'
YELLOW='\033[1;33m'
BLUE='\033[1;94m'
GRAY='\033[90m'
RESET='\033[0m'

# Banner
banner() {
    clear
    echo -e "${BLUE}"
    echo "  ╔═══════════════════════════════════════╗"
    echo "  ║      SARA v3.1 - Auto Installer      ║"
    echo "  ║   Simple Android Ransomware Attack   ║"
    echo "  ╚═══════════════════════════════════════╝"
    echo -e "${RESET}"
}

# Print with color
print_info() {
    echo -e "${BLUE}[*]${RESET} $1"
}

print_success() {
    echo -e "${GREEN}[✓]${RESET} $1"
}

print_error() {
    echo -e "${RED}[✗]${RESET} $1"
}

print_warning() {
    echo -e "${YELLOW}[!]${RESET} $1"
}

# Detect OS
detect_os() {
    if [ -n "$TERMUX_VERSION" ]; then
        OS="termux"
    elif [ -f /etc/os-release ]; then
        . /etc/os-release
        case "$ID" in
            ubuntu|debian|kali|parrot)
                OS="debian"
                ;;
            arch|manjaro)
                OS="arch"
                ;;
            fedora|centos|rhel)
                OS="redhat"
                ;;
            *)
                OS="unknown"
                ;;
        esac
    else
        OS="unknown"
    fi
    
    print_info "Detected OS: ${GREEN}$OS${RESET}"
}

# Check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Install for Termux
install_termux() {
    print_info "Installing dependencies for Termux..."
    
    # Update packages
    print_info "Updating package list..."
    pkg update -y || print_error "Failed to update packages"
    pkg upgrade -y || print_warning "Some packages failed to upgrade"
    
    # Install required packages
    print_info "Installing required packages..."
    pkg install -y python python-pip openjdk-17 wget curl git || {
        print_error "Failed to install base packages"
        exit 1
    }
    
    # Install apktool
    if ! command_exists apktool; then
        print_info "Installing apktool..."
        pkg install -y apktool || {
            print_warning "Package manager install failed, trying manual installation..."
            
            # Manual installation
            wget https://raw.githubusercontent.com/iBotPeaches/Apktool/master/scripts/linux/apktool -O $PREFIX/bin/apktool
            wget https://bitbucket.org/iBotPeaches/apktool/downloads/apktool_2.12.1.jar -O $PREFIX/bin/apktool.jar
            chmod +x $PREFIX/bin/apktool
            
            if command_exists apktool; then
                print_success "Apktool installed manually"
            else
                print_error "Failed to install apktool"
                exit 1
            fi
        }
    else
        print_success "Apktool already installed"
    fi
    
    # Install ImageMagick
    print_info "Installing ImageMagick..."
    pkg install -y imagemagick || print_warning "ImageMagick installation failed"
    
    # Install metasploit (optional)
    if ! command_exists msfconsole; then
        print_warning "Metasploit not found"
        read -p "Do you want to install Metasploit? (y/n): " install_msf
        if [[ $install_msf == "y" || $install_msf == "Y" ]]; then
            print_info "Installing Metasploit..."
            pkg install -y metasploit || {
                print_warning "Package install failed, trying from source..."
                cd $HOME
                git clone https://github.com/rapid7/metasploit-framework.git
                cd metasploit-framework
                gem install bundler
                bundle install
                print_success "Metasploit installed from source"
            }
        fi
    else
        print_success "Metasploit already installed"
    fi
}

# Install for Debian/Ubuntu
install_debian() {
    print_info "Installing dependencies for Debian/Ubuntu..."
    
    # Check for root/sudo
    if [ "$EUID" -ne 0 ]; then 
        print_error "Please run as root or with sudo"
        exit 1
    fi
    
    # Update packages
    print_info "Updating package list..."
    apt update || print_error "Failed to update packages"
    
    # Install required packages
    print_info "Installing required packages..."
    apt install -y python3 python3-pip openjdk-11-jdk wget curl git imagemagick || {
        print_error "Failed to install base packages"
        exit 1
    }
    
    # Install apktool
    if ! command_exists apktool; then
        print_info "Installing apktool..."
        
        # Try from repository first
        apt install -y apktool 2>/dev/null || {
            print_warning "Package manager install failed, trying manual installation..."
            
            # Manual installation
            wget https://raw.githubusercontent.com/iBotPeaches/Apktool/master/scripts/linux/apktool -O /usr/local/bin/apktool
            wget https://bitbucket.org/iBotPeaches/apktool/downloads/apktool_2.12.1.jar -O /usr/local/bin/apktool.jar
            chmod +x /usr/local/bin/apktool
            
            if command_exists apktool; then
                print_success "Apktool installed manually"
            else
                print_error "Failed to install apktool"
                exit 1
            fi
        }
    else
        print_success "Apktool already installed"
    fi
    
    # Install metasploit (optional)
    if ! command_exists msfconsole; then
        print_warning "Metasploit not found"
        read -p "Do you want to install Metasploit? (y/n): " install_msf
        if [[ $install_msf == "y" || $install_msf == "Y" ]]; then
            print_info "Installing Metasploit..."
            curl https://raw.githubusercontent.com/rapid7/metasploit-omnibus/master/config/templates/metasploit-framework-wrappers/msfupdate.erb > msfinstall
            chmod 755 msfinstall
            ./msfinstall
            rm msfinstall
        fi
    else
        print_success "Metasploit already installed"
    fi
}

# Install for Arch Linux
install_arch() {
    print_info "Installing dependencies for Arch Linux..."
    
    # Check for root/sudo
    if [ "$EUID" -ne 0 ]; then 
        print_error "Please run as root or with sudo"
        exit 1
    fi
    
    # Update packages
    print_info "Updating package list..."
    pacman -Sy || print_error "Failed to update packages"
    
    # Install required packages
    print_info "Installing required packages..."
    pacman -S --noconfirm python python-pip jdk11-openjdk wget curl git imagemagick || {
        print_error "Failed to install base packages"
        exit 1
    }
    
    # Install apktool
    if ! command_exists apktool; then
        print_info "Installing apktool..."
        
        pacman -S --noconfirm apktool 2>/dev/null || {
            print_warning "Package manager install failed, trying manual installation..."
            
            # Manual installation
            wget https://raw.githubusercontent.com/iBotPeaches/Apktool/master/scripts/linux/apktool -O /usr/local/bin/apktool
            wget https://bitbucket.org/iBotPeaches/apktool/downloads/apktool_2.12.1.jar -O /usr/local/bin/apktool.jar
            chmod +x /usr/local/bin/apktool
            
            if command_exists apktool; then
                print_success "Apktool installed manually"
            else
                print_error "Failed to install apktool"
                exit 1
            fi
        }
    else
        print_success "Apktool already installed"
    fi
    
    # Install metasploit (optional)
    if ! command_exists msfconsole; then
        print_warning "Metasploit not found"
        read -p "Do you want to install Metasploit from AUR? (y/n): " install_msf
        if [[ $install_msf == "y" || $install_msf == "Y" ]]; then
            print_info "Installing Metasploit..."
            pacman -S --noconfirm metasploit
        fi
    else
        print_success "Metasploit already installed"
    fi
}

# Install Python dependencies
install_python_deps() {
    print_info "Installing Python dependencies..."
    
    if [ -f "requirements.txt" ]; then
        if [ "$OS" = "termux" ]; then
            pip install -r requirements.txt --no-cache-dir || {
                print_error "Failed to install Python packages"
                exit 1
            }
        else
            if command_exists pip3; then
                pip3 install -r requirements.txt --break-system-packages 2>/dev/null || \
                pip3 install -r requirements.txt || {
                    print_error "Failed to install Python packages"
                    exit 1
                }
            else
                print_error "pip3 not found"
                exit 1
            fi
        fi
        print_success "Python dependencies installed"
    else
        print_error "requirements.txt not found!"
        exit 1
    fi
}

# Setup directories
setup_directories() {
    print_info "Setting up directories..."
    
    mkdir -p data/bin data/key data/tmp
    
    # Check if uber-apk-signer exists
    if [ ! -f "data/bin/ubersigner.jar" ]; then
        print_warning "uber-apk-signer not found in data/bin/"
        print_info "Please download uber-apk-signer.jar and place it in data/bin/ as ubersigner.jar"
        print_info "Download from: https://github.com/patrickfav/uber-apk-signer/releases"
    fi
    
    # Check if keystore exists
    if [ ! -f "data/key/debug.jks" ]; then
        print_warning "Debug keystore not found in data/key/"
        print_info "Generating debug keystore..."
        
        if command_exists keytool; then
            keytool -genkey -v -keystore data/key/debug.jks \
                -storepass debugging -alias debugging -keypass debugging \
                -keyalg RSA -keysize 2048 -validity 10000 \
                -dname "CN=Debug, OU=Debug, O=Debug, L=Debug, S=Debug, C=US" 2>/dev/null
            
            if [ -f "data/key/debug.jks" ]; then
                print_success "Debug keystore generated"
            else
                print_warning "Failed to generate keystore"
            fi
        else
            print_warning "keytool not found, cannot generate keystore"
        fi
    fi
    
    print_success "Directories setup complete"
}

# Verify installation
verify_installation() {
    print_info "Verifying installation..."
    
    local errors=0
    
    # Check Python
    if command_exists python3 || command_exists python; then
        print_success "Python installed"
    else
        print_error "Python not found"
        ((errors++))
    fi
    
    # Check Java
    if command_exists java; then
        print_success "Java installed"
    else
        print_error "Java not found"
        ((errors++))
    fi
    
    # Check apktool
    if command_exists apktool; then
        print_success "Apktool installed"
    else
        print_error "Apktool not found"
        ((errors++))
    fi
    
    # Check ImageMagick
    if command_exists convert || command_exists mogrify; then
        print_success "ImageMagick installed"
    else
        print_warning "ImageMagick not found (optional)"
    fi
    
    # Check Metasploit
    if command_exists msfconsole; then
        print_success "Metasploit installed"
    else
        print_warning "Metasploit not found (optional for trojan features)"
    fi
    
    if [ $errors -eq 0 ]; then
        print_success "All required dependencies installed!"
        return 0
    else
        print_error "Installation incomplete. $errors error(s) found."
        return 1
    fi
}

# Main installation
main() {
    banner
    
    print_info "Starting SARA v3.1 installation..."
    echo ""
    
    # Detect OS
    detect_os
    echo ""
    
    # Install based on OS
    case "$OS" in
        termux)
            install_termux
            ;;
        debian)
            install_debian
            ;;
        arch)
            install_arch
            ;;
        *)
            print_error "Unsupported OS: $OS"
            print_info "Supported: Termux, Debian/Ubuntu, Arch Linux"
            exit 1
            ;;
    esac
    
    echo ""
    
    # Setup directories
    setup_directories
    echo ""
    
    # Install Python dependencies
    install_python_deps
    echo ""
    
    # Verify installation
    verify_installation
    echo ""
    
    # Final message
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}╔════════════════════════════════════════════╗${RESET}"
        echo -e "${GREEN}║   Installation completed successfully!    ║${RESET}"
        echo -e "${GREEN}╚════════════════════════════════════════════╝${RESET}"
        echo ""
        print_info "Run the tool with: ${GREEN}python sara.py${RESET}"
        echo ""
        print_warning "Remember: This tool is for educational purposes only!"
    else
        echo -e "${RED}╔════════════════════════════════════════════╗${RESET}"
        echo -e "${RED}║     Installation completed with errors    ║${RESET}"
        echo -e "${RED}╚════════════════════════════════════════════╝${RESET}"
        echo ""
        print_info "Please check the errors above and try again"
    fi
}

# Run main function
main