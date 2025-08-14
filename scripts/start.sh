#!/bin/bash

# Script para iniciar el Asistente de Presupuestos HDL completo
# Autor: Corralón HDL
# Versión: 1.0.0

set -e

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

print_header() {
    echo -e "${BLUE}"
    echo "=================================================="
    echo "    Asistente de Presupuestos HDL - Inicio"
    echo "=================================================="
    echo -e "${NC}"
}

print_info() {
    echo -e "${BLUE}[INFO] $1${NC}"
}

print_success() {
    echo -e "${GREEN}[OK] $1${NC}"
}

print_error() {
    echo -e "${RED}[ERROR] $1${NC}"
}

# Verificar que estamos en el directorio correcto
if [ ! -f "README.md" ] || [ ! -d "frontend" ] || [ ! -d "backend" ]; then
    print_error "Por favor ejecuta este script desde el directorio raíz del proyecto"
    exit 1
fi

print_header

# Función para limpiar procesos al salir
cleanup() {
    print_info "Deteniendo servidores..."
    if [ ! -z "$BACKEND_PID" ]; then
        kill $BACKEND_PID 2>/dev/null || true
    fi
    if [ ! -z "$FRONTEND_PID" ]; then
        kill $FRONTEND_PID 2>/dev/null || true
    fi
    print_success "Servidores detenidos"
    exit 0
}

# Configurar trap para cleanup
trap cleanup SIGINT SIGTERM

# Iniciar backend
print_info "Iniciando backend..."
cd backend

# Verificar que el entorno virtual existe
if [ ! -d "venv" ]; then
    print_error "Entorno virtual no encontrado. Ejecuta ./scripts/setup.sh primero"
    exit 1
fi

# Activar entorno virtual e iniciar servidor
source venv/bin/activate
python src/main.py &
BACKEND_PID=$!

cd ..

# Esperar a que el backend inicie
print_info "Esperando a que el backend inicie..."
sleep 3

# Verificar que el backend está funcionando
if ! curl -f http://localhost:5000/ > /dev/null 2>&1; then
    print_error "El backend no pudo iniciarse correctamente"
    cleanup
    exit 1
fi

print_success "Backend iniciado en http://localhost:5000"

# Iniciar frontend
print_info "Iniciando frontend..."
cd frontend

# Verificar que las dependencias están instaladas
if [ ! -d "node_modules" ]; then
    print_error "Dependencias de Node.js no encontradas. Ejecuta ./scripts/setup.sh primero"
    cleanup
    exit 1
fi

# Iniciar servidor de desarrollo
npm run dev &
FRONTEND_PID=$!

cd ..

# Esperar a que el frontend inicie
print_info "Esperando a que el frontend inicie..."
sleep 5

print_success "Frontend iniciado en http://localhost:5173"

print_header
print_success "¡Aplicación iniciada exitosamente!"
echo ""
print_info "URLs de acceso:"
echo "  🌐 Frontend: http://localhost:5173"
echo "  🔧 Backend:  http://localhost:5000"
echo ""
print_info "Funcionalidades disponibles:"
echo "  💬 Chat conversacional"
echo "  📊 Panel de administración"
echo "  📄 Generación de PDFs"
echo "  🔍 Búsqueda de productos"
echo ""
print_info "Presiona Ctrl+C para detener ambos servidores"

# Mantener el script corriendo
while true; do
    sleep 1
    
    # Verificar que ambos procesos siguen corriendo
    if ! kill -0 $BACKEND_PID 2>/dev/null; then
        print_error "El backend se detuvo inesperadamente"
        cleanup
        exit 1
    fi
    
    if ! kill -0 $FRONTEND_PID 2>/dev/null; then
        print_error "El frontend se detuvo inesperadamente"
        cleanup
        exit 1
    fi
done

