"""
Seed script to populate the database with initial data from mock.js
Run this once to initialize the database with courses, games, testimonials, and schedule
"""

from motor.motor_asyncio import AsyncIOMotorClient
import asyncio
import os
from datetime import datetime
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables
ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

async def seed_database():
    print("🌱 Starting database seeding...")
    
    # Courses data
    courses = [
        {
            "title": "Python Programming",
            "description": "Learn Python from basics to advanced with game development projects",
            "ageGroup": "8-18 years",
            "duration": "6 months",
            "projects": "50+ games & apps",
            "icon": "code",
            "color": "blue",
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        },
        {
            "title": "C++ Programming",
            "description": "Master C++ fundamentals with interactive coding challenges",
            "ageGroup": "10-18 years",
            "duration": "6 months",
            "projects": "40+ projects",
            "icon": "cpu",
            "color": "purple",
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        },
        {
            "title": "HTML5 & CSS",
            "description": "Build beautiful websites from scratch with modern web design",
            "ageGroup": "8-18 years",
            "duration": "4 months",
            "projects": "30+ websites",
            "icon": "globe",
            "color": "green",
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        },
        {
            "title": "JavaScript",
            "description": "Create interactive web applications and games with JavaScript",
            "ageGroup": "10-18 years",
            "duration": "5 months",
            "projects": "35+ apps",
            "icon": "sparkles",
            "color": "yellow",
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        },
        {
            "title": "Game Development",
            "description": "Design and develop your own 2D & 3D games from scratch",
            "ageGroup": "8-18 years",
            "duration": "8 months",
            "projects": "60+ games",
            "icon": "gamepad2",
            "color": "red",
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        },
        {
            "title": "App Development",
            "description": "Build mobile applications and publish them on app stores",
            "ageGroup": "12-18 years",
            "duration": "7 months",
            "projects": "25+ apps",
            "icon": "smartphone",
            "color": "indigo",
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
    ]
    
    # Games data
    games = [
        {
            "name": "ChitChat",
            "image": "https://coding-stars.in/chitchat.png",
            "playStoreUrl": "https://play.google.com/store/apps/details?id=com.bhagyashree.chat",
            "category": "Social",
            "created_at": datetime.utcnow()
        },
        {
            "name": "Save the Alien",
            "image": "https://coding-stars.in/savethealien.jpeg",
            "playStoreUrl": "https://play.google.com/store/apps/details?id=com.bhagyashree3d.alien",
            "category": "3D Game",
            "created_at": datetime.utcnow()
        },
        {
            "name": "3D Enemy Shooter",
            "image": "https://coding-stars.in/3d%20enemy%20shooter.jpg",
            "playStoreUrl": "https://play.google.com/store/apps/details?id=com.splendid_crafts.ENEMYSHOOTER",
            "category": "3D Game",
            "created_at": datetime.utcnow()
        },
        {
            "name": "Racing Car 3D",
            "image": "https://coding-stars.in/racing%20car%203d.jpg",
            "playStoreUrl": "https://play.google.com/store/apps/details?id=com.bhagyashree.racingcar3d",
            "category": "Racing",
            "created_at": datetime.utcnow()
        },
        {
            "name": "Galaxy Star Shooter",
            "image": "https://coding-stars.in/galaxystarshooter.jpeg",
            "playStoreUrl": "https://play.google.com/store/apps/details?id=com.bhagyashree.galaxystarshooter",
            "category": "Arcade",
            "created_at": datetime.utcnow()
        },
        {
            "name": "Translato",
            "image": "https://coding-stars.in/translato.jpeg",
            "playStoreUrl": "https://play.google.com/store/apps/details?id=appinventor.ai_mahavirbhs2709parshwanath.Translatofinal",
            "category": "Utility",
            "created_at": datetime.utcnow()
        },
        {
            "name": "Find the Differences",
            "image": "https://coding-stars.in/findthedifferences.jpeg",
            "playStoreUrl": "https://play.google.com/store/apps/details?id=io.kodular.mahavirbhs2709parshwanath.Find_the_difference",
            "category": "Puzzle",
            "created_at": datetime.utcnow()
        },
        {
            "name": "Tic Tac Toe",
            "image": "https://coding-stars.in/tictactoe.jpeg",
            "playStoreUrl": "https://play.google.com/store/apps/details?id=com.bhagyashree.tictactoe",
            "category": "Puzzle",
            "created_at": datetime.utcnow()
        }
    ]
    
    # Testimonials data
    testimonials = [
        {
            "name": "Priya Sharma",
            "role": "Parent of 10-year-old",
            "content": "My daughter learned Python in just 6 months and created her own game! Dr. Bhagyashree's teaching method is exceptional.",
            "rating": 5,
            "avatar": "https://api.dicebear.com/7.x/avataaars/svg?seed=Priya",
            "is_approved": True,
            "created_at": datetime.utcnow()
        },
        {
            "name": "Rahul Patel",
            "role": "Parent of 14-year-old",
            "content": "The curriculum is well-structured and engaging. My son is now developing mobile apps and loving every moment of it.",
            "rating": 5,
            "avatar": "https://api.dicebear.com/7.x/avataaars/svg?seed=Rahul",
            "is_approved": True,
            "created_at": datetime.utcnow()
        },
        {
            "name": "Anita Desai",
            "role": "Parent of 12-year-old",
            "content": "Best coding platform for kids! The personalized attention and project-based learning approach is brilliant.",
            "rating": 5,
            "avatar": "https://api.dicebear.com/7.x/avataaars/svg?seed=Anita",
            "is_approved": True,
            "created_at": datetime.utcnow()
        },
        {
            "name": "Vikram Singh",
            "role": "Parent of 9-year-old",
            "content": "Dr. Bhagyashree is patient, knowledgeable, and makes coding fun. My son looks forward to every class!",
            "rating": 5,
            "avatar": "https://api.dicebear.com/7.x/avataaars/svg?seed=Vikram",
            "is_approved": True,
            "created_at": datetime.utcnow()
        }
    ]
    
    # Schedule data
    schedule = [
        {
            "day": "Monday",
            "slots": [
                {"time": "4:00 PM - 5:00 PM", "course": "Python Basics", "level": "Beginner"},
                {"time": "5:30 PM - 6:30 PM", "course": "Game Development", "level": "Intermediate"}
            ],
            "is_active": True,
            "created_at": datetime.utcnow()
        },
        {
            "day": "Tuesday",
            "slots": [
                {"time": "4:00 PM - 5:00 PM", "course": "HTML & CSS", "level": "Beginner"},
                {"time": "5:30 PM - 6:30 PM", "course": "JavaScript", "level": "Intermediate"}
            ],
            "is_active": True,
            "created_at": datetime.utcnow()
        },
        {
            "day": "Wednesday",
            "slots": [
                {"time": "4:00 PM - 5:00 PM", "course": "C++ Programming", "level": "Intermediate"},
                {"time": "5:30 PM - 6:30 PM", "course": "App Development", "level": "Advanced"}
            ],
            "is_active": True,
            "created_at": datetime.utcnow()
        },
        {
            "day": "Thursday",
            "slots": [
                {"time": "4:00 PM - 5:00 PM", "course": "Python Projects", "level": "Intermediate"},
                {"time": "5:30 PM - 6:30 PM", "course": "Web Development", "level": "Advanced"}
            ],
            "is_active": True,
            "created_at": datetime.utcnow()
        },
        {
            "day": "Friday",
            "slots": [
                {"time": "4:00 PM - 5:00 PM", "course": "Game Development", "level": "Beginner"},
                {"time": "5:30 PM - 6:30 PM", "course": "Project Showcase", "level": "All Levels"}
            ],
            "is_active": True,
            "created_at": datetime.utcnow()
        }
    ]
    
    # Clear existing data
    print("🗑️  Clearing existing data...")
    await db.courses.delete_many({})
    await db.games.delete_many({})
    await db.testimonials.delete_many({})
    await db.schedule.delete_many({})
    
    # Insert new data
    print("📚 Inserting courses...")
    await db.courses.insert_many(courses)
    print(f"✅ Inserted {len(courses)} courses")
    
    print("🎮 Inserting games...")
    await db.games.insert_many(games)
    print(f"✅ Inserted {len(games)} games")
    
    print("💬 Inserting testimonials...")
    await db.testimonials.insert_many(testimonials)
    print(f"✅ Inserted {len(testimonials)} testimonials")
    
    print("📅 Inserting schedule...")
    await db.schedule.insert_many(schedule)
    print(f"✅ Inserted {len(schedule)} schedule entries")
    
    print("\n🎉 Database seeding completed successfully!")
    
    # Close connection
    client.close()

if __name__ == "__main__":
    asyncio.run(seed_database())
