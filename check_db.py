#!/usr/bin/env python
"""
Script para verificar la conexión a PostgreSQL y mostrar información de la base de datos
"""
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'davegames_project.settings')
django.setup()

from django.db import connection
from games.models import Category, Game

def check_database():
    print("🎮 DaveGames - Verificación de Base de Datos PostgreSQL")
    print("=" * 60)
    
    try:
        # Verificar conexión
        with connection.cursor() as cursor:
            cursor.execute("SELECT version();")
            version = cursor.fetchone()[0]
            print(f"✅ Conexión exitosa a PostgreSQL")
            print(f"📊 Versión: {version}")
            
            # Verificar tablas
            cursor.execute("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public' 
                AND table_name LIKE 'games_%'
            """)
            tables = cursor.fetchall()
            print(f"📋 Tablas de games encontradas: {len(tables)}")
            for table in tables:
                print(f"   - {table[0]}")
            
        # Verificar datos
        categories_count = Category.objects.count()
        games_count = Game.objects.count()
        
        print(f"\n📈 Estadísticas de datos:")
        print(f"   - Categorías: {categories_count}")
        print(f"   - Juegos: {games_count}")
        
        if categories_count > 0:
            print(f"\n📂 Categorías disponibles:")
            for category in Category.objects.all():
                games_in_category = Game.objects.filter(category=category).count()
                print(f"   - {category.name}: {games_in_category} juego(s)")
                
        if games_count > 0:
            print(f"\n🎯 Juegos disponibles:")
            for game in Game.objects.all():
                print(f"   - {game.title} ({game.category.name}) - {game.release_date}")
                
        print(f"\n🔧 Configuración de la base de datos:")
        print(f"   - Host: {connection.settings_dict['HOST']}")
        print(f"   - Puerto: {connection.settings_dict['PORT']}")
        print(f"   - Base de datos: {connection.settings_dict['NAME']}")
        print(f"   - Usuario: {connection.settings_dict['USER']}")
        
        print(f"\n✅ ¡Todo está funcionando correctamente!")
        
    except Exception as e:
        print(f"❌ Error al conectar con la base de datos: {e}")
        return False
        
    return True

if __name__ == "__main__":
    check_database()