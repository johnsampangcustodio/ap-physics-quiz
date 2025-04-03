import os
from sqlalchemy import Column, Integer, String, Text, create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.future import select

# Database setup
DATABASE_URL = "sqlite+aiosqlite:///./quiz.db"
Base = declarative_base()

# Create async engine and session
engine = create_async_engine(DATABASE_URL, echo=True)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def get_db():
    """Dependency to get the database session"""
    async with async_session() as session:
        yield session

class Question(Base):
    """Model for questions in the database"""
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(Text, nullable=False)
    options = Column(Text, nullable=True)  # Multiple choice options as pipe-separated string
    correct_answer = Column(String, nullable=False)
    explanation = Column(Text, nullable=False)

    @classmethod
    async def get_all(cls, db: AsyncSession):
        """Get all questions from the database"""
        result = await db.execute(select(cls))
        return result.scalars().all()

    @classmethod
    async def get_by_id(cls, db: AsyncSession, question_id: int):
        """Get a question by ID"""
        result = await db.execute(select(cls).where(cls.id == question_id))
        return result.scalars().first()

async def init_db():
    """Initialize the database with tables and sample data"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # Add sample questions if the database is empty
    async with async_session() as session:
        # Check if questions table is empty
        result = await session.execute(select(Question))
        if not result.scalars().first():
            # Add sample questions
            sample_questions = [
                Question(
                    text="A block of mass 2 kg is sliding on a frictionless surface with a velocity of 3 m/s. What is its kinetic energy?",
                    options="3 J|6 J|9 J|18 J",
                    correct_answer="9 J",
                    explanation="Kinetic energy is calculated using the formula KE = (1/2)mv². For a 2 kg block moving at 3 m/s, KE = 0.5 × 2 × 3² = 9 J."
                ),
                Question(
                    text="A 5 kg object accelerates from rest to 10 m/s in 5 seconds. What is the magnitude of the net force acting on it?",
                    options="5 N|10 N|15 N|20 N",
                    correct_answer="10 N",
                    explanation="Using Newton's Second Law, F = ma. The acceleration is (change in velocity)/(time) = 10/5 = 2 m/s². Therefore, F = 5 kg × 2 m/s² = 10 N."
                ),
                Question(
                    text="A satellite is in a circular orbit around Earth at a distance of 3R from Earth's center, where R is Earth's radius. If the acceleration due to gravity at Earth's surface is g, what is the satellite's acceleration?",
                    options="g/3|g/6|g/9|g/12",
                    correct_answer="g/9",
                    explanation="The gravitational acceleration decreases with the square of the distance: a = g(R/r)². At a distance of 3R, a = g(R/3R)² = g/9."
                ),
                Question(
                    text="A simple pendulum has a period of 2 seconds. What is its length? (g = 9.8 m/s²)",
                    options="0.5 m|0.99 m|1.5 m|2.0 m",
                    correct_answer="0.99 m",
                    explanation="The period of a simple pendulum is T = 2π√(L/g). Solving for L: L = g(T/2π)² = 9.8(2/2π)² ≈ 0.99 m."
                ),
                Question(
                    text="Two masses m1 = 3 kg and m2 = 5 kg are connected by a massless string over a frictionless pulley. What is the acceleration of the system?",
                    options="1.225 m/s²|2.45 m/s²|4.9 m/s²|9.8 m/s²",
                    correct_answer="2.45 m/s²",
                    explanation="The acceleration is given by a = (m2-m1)g/(m1+m2) = (5-3)×9.8/(3+5) = 2.45 m/s²."
                ),
                Question(
                    text="A uniform rod of length L and mass M rotates about an axis perpendicular to the rod passing through one end. What is its moment of inertia?",
                    options="(1/3)ML²|(1/2)ML²|(2/3)ML²|ML²",
                    correct_answer="(1/3)ML²",
                    explanation="The moment of inertia for a uniform rod rotating about one end is I = (1/3)ML²."
                ),
                Question(
                    text="What is the work done by a constant force of 10 N acting on an object that moves 5 m in the direction of the force?",
                    options="20 J|30 J|40 J|50 J",
                    correct_answer="50 J",
                    explanation="Work is calculated as W = F·d·cosθ. When the force is in the same direction as displacement, cosθ = 1, so W = 10 N × 5 m = 50 J."
                ),
                Question(
                    text="A spring with spring constant k = 100 N/m is compressed by 0.2 m from its equilibrium position. What is the elastic potential energy stored in the spring?",
                    options="1 J|2 J|4 J|10 J",
                    correct_answer="2 J",
                    explanation="The elastic potential energy is calculated using U = (1/2)kx². U = 0.5 × 100 × 0.2² = 2 J."
                ),
                Question(
                    text="A mass on a spring is executing simple harmonic motion with a period of 0.5 seconds. If the amplitude of the motion is 0.1 m, what is the maximum speed of the mass?",
                    options="0.4π m/s|0.8π m/s|1.2π m/s|1.6π m/s",
                    correct_answer="0.4π m/s",
                    explanation="For simple harmonic motion, vmax = Aω, where ω = 2π/T. vmax = 0.1 × 2π/0.5 = 0.4π m/s."
                ),
                Question(
                    text="What is the centripetal acceleration of an object moving with a speed of 10 m/s in a circle of radius 5 m?",
                    options="5 m/s²|10 m/s²|15 m/s²|20 m/s²",
                    correct_answer="20 m/s²",
                    explanation="Centripetal acceleration is calculated using ac = v²/r = 10²/5 = 20 m/s²."
                )
                            Question(
                text="A car of mass 1000 kg is moving at 20 m/s. What is its momentum?",
                options="1000 kg·m/s|2000 kg·m/s|3000 kg·m/s|4000 kg·m/s",
                correct_answer="2000 kg·m/s",
                explanation="Momentum is calculated using p = mv. For a mass of 1000 kg moving at 20 m/s, p = 1000 × 20 = 2000 kg·m/s."
            ),
            Question(
                text="An object of mass 10 kg is moving in a circle of radius 2 m with a speed of 4 m/s. What is its centripetal force?",
                options="10 N|20 N|40 N|80 N",
                correct_answer="20 N",
                explanation="Centripetal force is given by Fc = mv²/r. For a mass of 10 kg moving at 4 m/s in a circle of radius 2 m, Fc = 10 × 4² / 2 = 20 N."
            ),
            Question(
                text="A 50 N force is applied to an object at an angle of 30° with the horizontal. What is the horizontal component of the force?",
                options="25 N|35 N|40 N|45 N",
                correct_answer="43.3 N",
                explanation="The horizontal component of the force is given by Fh = F cosθ. Fh = 50 N × cos(30°) ≈ 43.3 N."
            ),
            Question(
                text="An object is dropped from a height of 5 meters. Neglecting air resistance, what is the object's velocity just before it hits the ground? (g = 9.8 m/s²)",
                options="5 m/s|7 m/s|9 m/s|10 m/s",
                correct_answer="9.8 m/s",
                explanation="Using the equation v = √(2gh), v = √(2 × 9.8 × 5) ≈ 9.8 m/s."
            ),
            Question(
                text="A block of mass 2 kg is placed on a frictionless surface. A force of 10 N is applied horizontally to the block. What is the acceleration of the block?",
                options="2 m/s²|3 m/s²|4 m/s²|5 m/s²",
                correct_answer="5 m/s²",
                explanation="Using Newton's Second Law, F = ma. The acceleration is a = F/m = 10 N / 2 kg = 5 m/s²."
            ),
            Question(
                text="A satellite is orbiting Earth at a height of 2R above the Earth's surface. What is the acceleration due to gravity at the satellite's location?",
                options="g/2|g/4|g/8|g/16",
                correct_answer="g/4",
                explanation="The gravitational acceleration decreases with the square of the distance from the center of the Earth. At a height of 2R, the gravitational acceleration is a = g(1/(3))² = g/4."
            ),
            Question(
                text="A particle moves in simple harmonic motion with an amplitude of 0.5 m and a frequency of 2 Hz. What is the maximum acceleration of the particle?",
                options="4π² m/s²|8π² m/s²|2π² m/s²|π² m/s²",
                correct_answer="4π² m/s²",
                explanation="The maximum acceleration in SHM is given by a_max = ω²A, where ω = 2πf. Thus, a_max = (2π × 2)² × 0.5 = 4π² m/s²."
            ),
            Question(
                text="What is the angular velocity of a wheel rotating at 60 rpm?",
                options="2π/60 rad/s|π rad/s|π/30 rad/s|2π rad/s",
                correct_answer="2π/60 rad/s",
                explanation="Angular velocity ω is related to the rotation rate in revolutions per minute by ω = 2π × (rpm/60). For 60 rpm, ω = 2π/60 rad/s."
            ),
            Question(
                text="A 2 kg object is moving in a circle with a radius of 1.5 m and a speed of 4 m/s. What is its centripetal acceleration?",
                options="4/3 m/s²|6/3 m/s²|16/3 m/s²|5/3 m/s²",
                correct_answer="16/3 m/s²",
                explanation="Centripetal acceleration is calculated as a_c = v² / r. For v = 4 m/s and r = 1.5 m, a_c = 4² / 1.5 = 16/3 m/s²."
            ),
            Question(
                text="A 10 kg object is at rest on a horizontal surface. What is the normal force acting on the object?",
                options="10 N|20 N|0 N|98 N",
                correct_answer="98 N",
                explanation="The normal force is equal to the weight of the object, which is F_N = mg = 10 kg × 9.8 m/s² = 98 N."
            ),
            Question(
                text="A block is sliding down a frictionless incline at an angle of 30°. What is the acceleration of the block?",
                options="5 m/s²|9.8 m/s²|4.9 m/s²|10 m/s²",
                correct_answer="4.9 m/s²",
                explanation="The acceleration down the incline is given by a = g sinθ. For θ = 30°, a = 9.8 × sin(30°) = 4.9 m/s²."
            ),
            Question(
                text="What is the period of a mass-spring system with a spring constant of 200 N/m and a mass of 4 kg?",
                options="0.5 s|1 s|2 s|4 s",
                correct_answer="1 s",
                explanation="The period of a mass-spring system is given by T = 2π√(m/k). For m = 4 kg and k = 200 N/m, T = 2π√(4/200) ≈ 1 s."
            ),
            Question(
                text="An object with mass 3 kg is placed on a frictionless horizontal surface. What is the object's acceleration when a force of 15 N is applied to it?",
                options="2 m/s²|3 m/s²|4 m/s²|5 m/s²",
                correct_answer="5 m/s²",
                explanation="Using Newton's Second Law, F = ma. The acceleration is a = F/m = 15 N / 3 kg = 5 m/s²."
            ),
            Question(
                text="A particle is rotating with a constant angular acceleration of 2 rad/s². What is the angular velocity after 5 seconds?",
                options="5 rad/s|10 rad/s|15 rad/s|20 rad/s",
                correct_answer="10 rad/s",
                explanation="Angular velocity is given by ω = ω₀ + αt. With initial angular velocity ω₀ = 0 and α = 2 rad/s², after 5 seconds, ω = 0 + 2 × 5 = 10 rad/s."
            ),
            Question(
                text="A wheel with moment of inertia 2 kg·m² is subjected to a torque of 6 N·m. What is the angular acceleration of the wheel?",
                options="2 rad/s²|3 rad/s²|4 rad/s²|5 rad/s²",
                correct_answer="3 rad/s²",
                explanation="The angular acceleration is given by α = τ/I. With τ = 6 N·m and I = 2 kg·m², α = 6 / 2 = 3 rad/s²."
            ),
            Question(
                text="The work-energy theorem states that the work done on an object is equal to its change in kinetic energy. If a 2 kg object speeds up from 0 m/s to 10 m/s, what is the work done on it?",
                options="50 J|100 J|150 J|200 J",
                correct_answer="100 J",
                explanation="The change in kinetic energy is ΔKE = (1/2)mv² - (1/2)mu². For m = 2 kg and v = 10 m/s, ΔKE = 1/2 × 2 × 10² = 100 J."
            ),
            Question(
                text="A mass is attached to a spring and is undergoing simple harmonic motion. If the amplitude is doubled, what happens to the maximum speed of the mass?",
                options="Doubles|Halves|Quadruples|Stays the same",
                correct_answer="Doubles",
                explanation="The maximum speed in simple harmonic motion is given by vmax = Aω. Since ω is constant, doubling the amplitude will double the maximum speed."
            )
                        Question(
                text="A disk with mass M and radius R is rotating about an axis through its center. A torque τ is applied to it, resulting in an angular acceleration α. What is the angular velocity after time t?",
                options="ω = αt|ω = τt/I|ω = (τt)/M|ω = τt/R",
                correct_answer="ω = τt/I",
                explanation="The angular velocity is given by the equation ω = τt/I, where I is the moment of inertia of the disk. For a solid disk, I = 1/2MR²."
            ),
            Question(
                text="A mass m slides down a frictionless incline at an angle of θ. If the object reaches the bottom with velocity v, what is the work done by gravity on the object?",
                options="W = mgh|W = mg sin(θ)h|W = mgh cos(θ)|W = mg cos(θ)h",
                correct_answer="W = mgh",
                explanation="The work done by gravity is the change in potential energy, W = mgh, where h is the vertical height of the incline."
            ),
            Question(
                text="A block of mass 2 kg is attached to a spring with spring constant k = 500 N/m. The block oscillates with an amplitude of 0.1 m. What is the maximum kinetic energy of the block?",
                options="2.5 J|5.0 J|10.0 J|20.0 J",
                correct_answer="2.5 J",
                explanation="The maximum kinetic energy is equal to the maximum potential energy stored in the spring, which is given by KE_max = (1/2)kA². Thus, KE_max = (1/2) × 500 × (0.1)² = 2.5 J."
            ),
            Question(
                text="A satellite is in a circular orbit around the Earth at a distance of 2R from the Earth's center. What is the gravitational force acting on the satellite?",
                options="F = GmM/R²|F = GmM/4R²|F = GmM/2R²|F = GmM/3R²",
                correct_answer="F = GmM/4R²",
                explanation="The gravitational force between two masses is given by F = GmM/r². At a distance of 2R from the Earth's center, F = GmM/(2R)² = GmM/4R²."
            ),
            Question(
                text="A 10 kg object is suspended from a spring. If the spring constant is 200 N/m, how much does the spring stretch when the object is in equilibrium?",
                options="0.1 m|0.2 m|0.5 m|1.0 m",
                correct_answer="0.5 m",
                explanation="Using Hooke's Law, F = kx, where F is the weight of the object (mg), k is the spring constant, and x is the displacement. Solving for x, x = mg/k = 10 × 9.8 / 200 = 0.49 m, approximately 0.5 m."
            ),
            Question(
                text="A 5 kg mass is rotating in a circle of radius 2 m at a constant speed of 3 m/s. What is the centripetal force acting on the mass?",
                options="5 N|7.5 N|15 N|25 N",
                correct_answer="7.5 N",
                explanation="Centripetal force is given by Fc = mv²/r. For m = 5 kg, v = 3 m/s, and r = 2 m, Fc = 5 × 3² / 2 = 7.5 N."
            ),
            Question(
                text="A 3 kg mass is moving with velocity 4 m/s in a circular path with a radius of 1.5 m. What is the angular momentum of the mass about the center of the circle?",
                options="12 kg·m²/s|18 kg·m²/s|24 kg·m²/s|36 kg·m²/s",
                correct_answer="18 kg·m²/s",
                explanation="Angular momentum L is given by L = mvr. For m = 3 kg, v = 4 m/s, and r = 1.5 m, L = 3 × 4 × 1.5 = 18 kg·m²/s."
            ),
            Question(
                text="A rigid body with moment of inertia I is subjected to a torque τ. What is the angular acceleration α of the body?",
                options="α = τ/I|α = Iτ|α = τ/I²|α = Iτ²",
                correct_answer="α = τ/I",
                explanation="The angular acceleration is given by the equation α = τ/I, where τ is the applied torque and I is the moment of inertia."
            ),
            Question(
                text="A particle moves along a straight line with constant acceleration. If its initial velocity is 0 and it accelerates for 5 seconds, reaching a velocity of 10 m/s, what is the acceleration of the particle?",
                options="1 m/s²|2 m/s²|3 m/s²|4 m/s²",
                correct_answer="2 m/s²",
                explanation="Using the equation v = u + at, where u is the initial velocity, v is the final velocity, a is acceleration, and t is time. Solving for a, a = (v - u) / t = (10 - 0) / 5 = 2 m/s²."
            ),
            Question(
                text="An object is moving with constant speed along a horizontal circle. If the radius of the circle is doubled and the speed is quadrupled, by what factor does the centripetal force change?",
                options="2|4|8|16",
                correct_answer="16",
                explanation="Centripetal force is given by Fc = mv²/r. If the radius is doubled and the speed is quadruled, the centripetal force increases by a factor of (4²)/(2) = 16."
            ),
            Question(
                text="A rotating disc with radius R and mass M has a moment of inertia I = 1/2MR². If a constant torque τ is applied to the disc, what is the angular acceleration?",
                options="α = 2τ/MR²|α = τ/MR²|α = 2τ/3MR²|α = τ/2MR²",
                correct_answer="α = 2τ/MR²",
                explanation="Using the equation τ = Iα and I = 1/2MR², the angular acceleration α = τ / (1/2MR²) = 2τ / MR²."
            ),
            Question(
                text="A spring with spring constant k = 100 N/m is compressed by 0.5 m. How much work is required to compress the spring?",
                options="12.5 J|25 J|50 J|100 J",
                correct_answer="12.5 J",
                explanation="The work done in compressing a spring is given by W = (1/2)kx². For k = 100 N/m and x = 0.5 m, W = (1/2) × 100 × (0.5)² = 12.5 J."
            ),
            Question(
                text="Two masses m1 and m2 are connected by a frictionless pulley. If m1 = 10 kg and m2 = 5 kg, and the system accelerates with acceleration a, what is the value of a?",
                options="2.5 m/s²|3.5 m/s²|4.0 m/s²|5.0 m/s²",
                correct_answer="3.5 m/s²",
                explanation="Using Newton's second law, a = (m2 - m1)g / (m1 + m2). For m1 = 10 kg, m2 = 5 kg, and g = 9.8 m/s², a = (5 - 10) × 9.8 / (10 + 5) = -3.5 m/s²."
            ),
            Question(
                text="A rotating wheel with angular velocity ω₀ = 10 rad/s accelerates at a constant rate of α = 2 rad/s². What is the angular velocity after 5 seconds?",
                options="20 rad/s|30 rad/s|40 rad/s|50 rad/s",
                correct_answer="20 rad/s",
                explanation="The angular velocity is given by ω = ω₀ + αt. With ω₀ = 10 rad/s, α = 2 rad/s², and t = 5 s, ω = 10 + 2 × 5 = 20 rad/s."
            ),
            Question(
                text="A 20 kg object is dropped from a height of 10 m. How much kinetic energy does it have just before it hits the ground? (g = 9.8 m/s²)",
                options="100 J|150 J|200 J|250 J",
                correct_answer="200 J",
                explanation="The potential energy at the top is converted into kinetic energy. The potential energy is given by PE = mgh. For m = 20 kg, g = 9.8 m/s², and h = 10 m, PE = 20 × 9.8 × 10 = 200 J."
            ),
            Question(
                text="A rigid rod of length L and mass M rotates about an axis through one end. What is the moment of inertia of the rod?",
                options="(1/12)ML²|(1/2)ML²|(1/3)ML²|ML²",
                correct_answer="(1/3)ML²",
                explanation="The moment of inertia of a uniform rod rotating about an axis through one end is given by I = (1/3)ML²."
            ),
            Question(
                text="A solid sphere with mass M and radius R rolls without slipping down an incline. What is the acceleration of the sphere along the incline?",
                options="g/2|g/3|g/4|g/5",
                correct_answer="g/5",
                explanation="For rolling without slipping, the acceleration is given by a = g/(1 + I/MR²), where I = 2/5MR² for a solid sphere. Therefore, a = g/(1 + 2/5) = g/5."
            ),
            Question(
                text="A particle undergoes simple harmonic motion with a period of T. If the amplitude of the motion is doubled, by what factor does the maximum velocity change?",
                options="2|4|1/2|1/4",
                correct_answer="2",
                explanation="The maximum velocity is given by vmax = Aω. Since ω = 2π/T and amplitude is doubled, vmax will double as well."
            )
            ]
            
            for question in sample_questions:
                session.add(question)
            
            await session.commit() 