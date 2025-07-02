#!/usr/bin/env python3
"""
Script de prueba para verificar que la pasarela de pago funciona en local
"""

import os
import sys

def verificar_configuracion():
    """Verifica que la configuración esté correcta"""
    print("🔍 Verificando configuración...")
    
    # Verificar archivos necesarios
    archivos_necesarios = [
        'main.py',
        'utils/PagoTPVSantander.py',
        'utils/PagoHandler.py',
        'utils/tpv_routes.py',
        'utils/pago_registry.py',
        'dorsal_solidario/dorsalsolidario_screen.py',
        '.env'
    ]
    
    for archivo in archivos_necesarios:
        if os.path.exists(archivo):
            print(f"✅ {archivo}")
        else:
            print(f"❌ {archivo} - NO ENCONTRADO")
            return False
    
    # Verificar variables de entorno
    from dotenv import load_dotenv
    load_dotenv()
    
    variables_necesarias = ['MERCHANT_CODE', 'TERMINAL_TPV', 'FIRMA_SECRETA']
    
    for var in variables_necesarias:
        valor = os.getenv(var)
        if valor:
            print(f"✅ {var}: {valor[:10]}...")
        else:
            print(f"❌ {var} - NO CONFIGURADA")
            return False
    
    # Verificar EXTERNAL_URL
    external_url = os.getenv('EXTERNAL_URL')
    if external_url and not external_url.startswith('https://tu-dominio'):
        print(f"🌍 EXTERNAL_URL: {external_url}")
        print("⚠️ MODO PRODUCCIÓN - Para local, comenta esta línea en .env")
    else:
        print("🏠 MODO LOCAL - EXTERNAL_URL comentada o no configurada")
    
    return True

def test_import():
    """Prueba que las importaciones funcionen"""
    print("\n🔍 Verificando importaciones...")
    
    try:
        from utils.PagoTPVSantander import PagoTPVSantander
        print("✅ PagoTPVSantander")
        
        from utils.tpv_routes import manejar_rutas_tpv
        print("✅ tpv_routes")
        
        from utils.pago_registry import registrar_pago_activo
        print("✅ pago_registry")
        
        from dorsal_solidario.dorsalsolidario_screen import DorsalSolidarioScreen
        print("✅ DorsalSolidarioScreen")
        
        return True
        
    except ImportError as e:
        print(f"❌ Error de importación: {e}")
        return False

def test_pago_instance():
    """Prueba crear una instancia de pago"""
    print("\n🔍 Probando instancia de pago...")
    
    try:
        from utils.PagoTPVSantander import PagoTPVSantander
        
        pago = PagoTPVSantander(
            concepto="Test Dorsal Solidario",
            importe=5.0,
            entorno_test=True,  # Modo pruebas
        )
        
        print(f"✅ Instancia creada")
        print(f"📋 Número de pedido: {pago.numero_pedido}")
        print(f"🌍 Entorno detectado: {'LOCAL' if pago.es_local else 'PRODUCCIÓN'}")
        print(f"🔗 Base URL: {pago.base_url}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error creando instancia: {e}")
        return False

def main():
    """Función principal de prueba"""
    print("🧪 PRUEBA DE CONFIGURACIÓN - Pasarela de Pago TPV")
    print("=" * 60)
    
    # Verificar configuración
    if not verificar_configuracion():
        print("\n❌ FALLO EN CONFIGURACIÓN")
        return False
    
    # Verificar importaciones  
    if not test_import():
        print("\n❌ FALLO EN IMPORTACIONES")
        return False
        
    # Probar instancia de pago
    if not test_pago_instance():
        print("\n❌ FALLO CREANDO INSTANCIA DE PAGO")
        return False
    
    print("\n✅ TODAS LAS PRUEBAS PASARON")
    print("\n🚀 Para probar la aplicación completa ejecuta:")
    print("   python main.py")
    print("\n🎯 Luego ve a http://localhost/btn_dorsal_solidario y haz clic en PAGAR")
    
    return True

if __name__ == "__main__":
    if main():
        sys.exit(0)
    else:
        sys.exit(1)