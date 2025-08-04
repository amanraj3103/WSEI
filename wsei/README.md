# WSEI Academy Platform

A modern student management system built with Next.js, TypeScript, and Prisma. This platform provides a comprehensive solution for student registration, authentication, and administrative management.

## Features

### 🎓 Student Features
- **Secure Login**: Login with registration number or email
- **Profile Management**: View personal and academic information
- **Responsive Dashboard**: Modern, mobile-friendly interface

### 👨‍💼 Admin Features
- **Student Registration**: Register new students with automatic email generation and unique registration numbers
- **Student Database Management**: Complete overview of all registered students
- **Advanced Search & Filtering**: Search by name, registration number, email, or filter by course/semester
- **Sorting Capabilities**: Sort by registration number, name, course, semester, or enrollment date
- **Statistics Dashboard**: Real-time statistics and insights
- **Student Status Management**: Track active, inactive, graduated, and suspended students
- **Student Deletion**: Permanently delete student profiles from the database with confirmation modal

### 🔧 Technical Features
- **Modern Tech Stack**: Next.js 14, TypeScript, Tailwind CSS
- **Database Integration**: PostgreSQL with Prisma ORM
- **Secure Authentication**: bcrypt password hashing
- **Responsive Design**: Mobile-first approach
- **Vercel Ready**: Optimized for deployment on Vercel

## Tech Stack

- **Frontend**: Next.js 14, React 18, TypeScript
- **Styling**: Tailwind CSS
- **Database**: PostgreSQL
- **ORM**: Prisma
- **Authentication**: bcryptjs
- **Icons**: Lucide React
- **Deployment**: Vercel

## Prerequisites

Before you begin, ensure you have the following installed:
- Node.js (v18 or higher)
- npm or yarn
- PostgreSQL database

## Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd wsei-university-platform
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Set up environment variables**
   ```bash
   cp env.example .env.local
   ```
   
   Update the `.env.local` file with your database credentials:
   ```env
   DATABASE_URL="postgresql://username:password@localhost:5432/wsei_university"
   NEXTAUTH_URL="http://localhost:3000"
   NEXTAUTH_SECRET="your-secret-key-here"
   ADMIN_USERNAME="admin"
   ADMIN_PASSWORD="admin123"
   ADMIN_EMAIL="admin@wsei.pl"
   ```

4. **Set up the database**
   ```bash
   # Generate Prisma client
   npm run db:generate
   
   # Push schema to database
   npm run db:push
   ```

5. **Run the development server**
   ```bash
   npm run dev
   ```

6. **Open your browser**
   Navigate to [http://localhost:3000](http://localhost:3000)

## Usage

### Admin Student Registration
1. Login as admin using admin credentials
2. Click "Register New Student" button in the admin dashboard
3. Fill in all required fields:
   - Personal information (name, date of birth)
   - Academic information (course, semester)
4. **Auto-generated credentials**:
   - **Email**: `firstname.lastname@student.wsei.pl`
   - **Password**: `firstname@123`
5. Submit the form to create the student account (registration number will be auto-generated)
6. **Duplicate Prevention**: The system will block registration if:
   - Email already exists in the database
   - A student with the same first and last name already exists

### Student Login
1. Use your registration number or email and password to log in
2. **Password format**: `firstname@123` (e.g., john@123, amar@123)
3. Access your personalized dashboard
4. View your academic information and profile details

### Admin Access
1. Use the admin credentials configured in your environment variables
2. Access the comprehensive admin dashboard
3. Manage all student records with advanced filtering and sorting

## Database Schema

### Users Table
- `id`: Unique identifier
- `email`: Email address (unique)
- `username`: Username (unique)
- `password`: Hashed password
- `role`: User role (STUDENT/ADMIN)
- `createdAt`: Account creation timestamp
- `updatedAt`: Last update timestamp

### Students Table
- `id`: Unique identifier
- `registrationNo`: Unique registration number (auto-generated)
- `firstName`: Student's first name
- `lastName`: Student's last name
- `dateOfBirth`: Date of birth
- `courseOfStudy`: Academic course/program
- `semester`: Current semester
- `email`: Contact email
- `phone`: Contact phone (optional)
- `address`: Physical address (optional)
- `enrollmentDate`: Date of enrollment
- `status`: Student status (ACTIVE/INACTIVE/GRADUATED/SUSPENDED)
- `userId`: Reference to user account

## API Endpoints

### Authentication
- `POST /api/auth/login` - User login
- `POST /api/auth/signup` - Student registration

### Data Management
- `GET /api/students` - Fetch all students (admin only)


## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `DATABASE_URL` | PostgreSQL connection string | Yes |
| `NEXTAUTH_URL` | Application URL | Yes |
| `NEXTAUTH_SECRET` | Secret key for NextAuth | Yes |
| `ADMIN_USERNAME` | Admin login username | Yes |
| `ADMIN_PASSWORD` | Admin login password | Yes |
| `ADMIN_EMAIL` | Admin email address | Yes |

