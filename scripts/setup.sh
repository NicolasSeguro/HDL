#!/bin/bash

# Script de instalación automática para Asistente de Presupuestos HDL
# Autor: Corralón HDL
# Versión: 1.0.0

set -e  # Salir si hay errores

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Funciones de utilidad
print_header() {
    echo -e "${BLUE}"
    echo "=================================================="
    echo "  Asistente de Presupuestos HDL - Instalación"
    echo "=================================================="
    echo -e "${NC}"
}

print_step() {
    echo -e "${YELLOW}[PASO] $1${NC}"
}

print_success() {
    echo -e "${GREEN}[OK] $1${NC}"
}

print_error() {
    echo -e "${RED}[ERROR] $1${NC}"
}

print_info() {
    echo -e "${BLUE}[INFO] $1${NC}"
}

# Verificar requisitos del sistema
check_requirements() {
    print_step "Verificando requisitos del sistema..."
    
    # Verificar Node.js
    if ! command -v node &> /dev/null; then
        print_error "Node.js no está instalado. Por favor instala Node.js 18+ desde https://nodejs.org/"
        exit 1
    fi
    
    NODE_VERSION=$(node --version | cut -d'v' -f2 | cut -d'.' -f1)
    if [ "$NODE_VERSION" -lt 18 ]; then
        print_error "Node.js versión 18+ requerida. Versión actual: $(node --version)"
        exit 1
    fi
    print_success "Node.js $(node --version) ✓"
    
    # Verificar Python
    if ! command -v python3 &> /dev/null; then
        print_error "Python 3 no está instalado. Por favor instala Python 3.11+"
        exit 1
    fi
    
    PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1-2)
    print_success "Python $(python3 --version) ✓"
    
    # Verificar pip
    if ! command -v pip3 &> /dev/null; then
        print_error "pip3 no está instalado. Por favor instala pip3"
        exit 1
    fi
    print_success "pip3 $(pip3 --version | cut -d' ' -f2) ✓"
    
    # Verificar npm
    if ! command -v npm &> /dev/null; then
        print_error "npm no está instalado. Por favor instala npm"
        exit 1
    fi
    print_success "npm $(npm --version) ✓"
    
    print_success "Todos los requisitos están satisfechos"
}

# Configurar backend
setup_backend() {
    print_step "Configurando backend..."
    
    cd backend
    
    # Crear entorno virtual
    print_info "Creando entorno virtual de Python..."
    python3 -m venv venv
    
    # Activar entorno virtual
    source venv/bin/activate
    
    # Actualizar pip
    print_info "Actualizando pip..."
    pip install --upgrade pip
    
    # Instalar dependencias
    print_info "Instalando dependencias de Python..."
    pip install -r requirements.txt
    
    # Crear directorios necesarios
    mkdir -p ../data/budgets ../data/knowledge ../logs
    
    # Crear archivo .env si no existe
    if [ ! -f .env ]; then
        print_info "Creando archivo de configuración .env..."
        cat > .env << EOF
# Configuración del servidor
FLASK_ENV=development
FLASK_DEBUG=True
HOST=0.0.0.0
PORT=5000

# APIs HDL Zomatik
HDL_API_BASE=https://hdl.zomatik.com/ws_web.php
HDL_API_TIMEOUT=30

# Configuración de archivos
UPLOAD_FOLDER=../data/uploads
MAX_CONTENT_LENGTH=16777216

# Logging
LOG_LEVEL=INFO
LOG_FILE=../logs/app.log
EOF
    fi
    
    cd ..
    print_success "Backend configurado correctamente"
}

# Configurar frontend
setup_frontend() {
    print_step "Configurando frontend..."
    
    cd frontend
    
    # Instalar dependencias
    print_info "Instalando dependencias de Node.js..."
    npm install
    
    # Crear build de prueba
    print_info "Creando build de prueba..."
    npm run build
    
    cd ..
    print_success "Frontend configurado correctamente"
}

# Ejecutar tests
run_tests() {
    print_step "Ejecutando tests básicos..."
    
    # Test del backend
    print_info "Probando backend..."
    cd backend
    source venv/bin/activate
    
    # Iniciar servidor en background
    python src/main.py &
    BACKEND_PID=$!
    
    # Esperar a que el servidor inicie
    sleep 5
    
    # Probar endpoint básico
    if curl -f http://localhost:5000/ > /dev/null 2>&1; then
        print_success "Backend responde correctamente"
    else
        print_error "Backend no responde"
        kill $BACKEND_PID 2>/dev/null || true
        exit 1
    fi
    
    # Terminar servidor
    kill $BACKEND_PID 2>/dev/null || true
    
    cd ..
    
    # Test del frontend
    print_info "Probando frontend..."
    cd frontend
    
    # Verificar que el build fue exitoso
    if [ -d "dist" ]; then
        print_success "Frontend build exitoso"
    else
        print_error "Frontend build falló"
        exit 1
    fi
    
    cd ..
    print_success "Todos los tests pasaron"
}

# Función principal
main() {
    print_header
    
    # Verificar que estamos en el directorio correcto
    if [ ! -f "README.md" ] || [ ! -d "frontend" ] || [ ! -d "backend" ]; then
        print_error "Por favor ejecuta este script desde el directorio raíz del proyecto"
        exit 1
    fi
    
    print_info "Iniciando instalación automática..."
    
    check_requirements
    setup_backend
    setup_frontend
    run_tests
    
    print_header
    print_success "¡Instalación completada exitosamente!"
    echo ""
    print_info "Para iniciar el proyecto:"
    echo "  1. Backend:  ./scripts/start-backend.sh"
    echo "  2. Frontend: ./scripts/start-frontend.sh"
    echo "  3. O ambos:  ./scripts/start.sh"
    echo ""
    print_info "URLs de acceso:"
    echo "  - Frontend: http://localhost:5173"
    echo "  - Backend:  http://localhost:5000"
    echo ""
    print_info "Documentación disponible en:"
    echo "  - README.md"
    echo "  - INSTALL.md"
    echo "  - ARCHITECTURE.md"
    echo "  - docs/"
    echo ""
    print_success "¡Disfruta usando el Asistente de Presupuestos HDL!"
}

# Ejecutar función principal
main "$@"

