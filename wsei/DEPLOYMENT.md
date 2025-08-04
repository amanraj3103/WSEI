# WSEI Academy Platform - Production Deployment Guide

## 🚀 Quick Start

### 1. Set up Vercel Postgres Database

1. **Go to Vercel Dashboard**: https://vercel.com/dashboard
2. **Select your WSEI project**
3. **Go to Storage tab**
4. **Click "Create Database"**
5. **Select "Postgres"**
6. **Choose a plan** (Hobby plan is free for development)
7. **Select a region** (choose closest to your users)
8. **Click "Create"**

### 2. Configure Environment Variables

In your Vercel project settings, add these environment variables:

```bash
# Database URL (from Vercel Postgres)
DATABASE_URL="postgresql://username:password@host:port/database"

# NextAuth (generate a secure secret)
NEXTAUTH_SECRET="your-secure-secret-key-here"

# Admin credentials (change these in production)
ADMIN_USERNAME="admin"
ADMIN_PASSWORD="admin123"
ADMIN_EMAIL="admin@wsei.pl"
```

### 3. Deploy and Setup Database

```bash
# Deploy to Vercel
npx vercel --prod

# Setup production database (run this after deployment)
npm run setup-production
```

## 📋 Environment Variables

### Required Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `DATABASE_URL` | PostgreSQL connection string | `postgresql://user:pass@host:5432/db` |
| `NEXTAUTH_SECRET` | Secret for session encryption | `your-secure-secret-key` |

### Optional Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `ADMIN_USERNAME` | Admin login username | `admin` |
| `ADMIN_PASSWORD` | Admin login password | `admin123` |
| `ADMIN_EMAIL` | Admin email address | `admin@wsei.pl` |

## 🗄️ Database Setup

### Local Development (SQLite)

```bash
# Use SQLite for local development
DATABASE_URL="file:./dev.db"

# Initialize local database
npm run db:push
npm run init-admin
npm run init-student
```

### Production (PostgreSQL)

```bash
# Use PostgreSQL for production
DATABASE_URL="postgresql://username:password@host:port/database"

# Setup production database
npm run setup-production
```

## 🔧 Database Commands

```bash
# Generate Prisma client
npm run db:generate

# Push schema to database
npm run db:push

# Open Prisma Studio (local only)
npm run db:studio

# Initialize admin user
npm run init-admin

# Initialize test student
npm run init-student

# Update student passwords
npm run update-passwords

# Setup production database
npm run setup-production
```

## 🌐 Deployment URLs

- **Production**: https://wsei-npvzkxfwp-amanraj3103s-projects.vercel.app
- **Vercel Dashboard**: https://vercel.com/dashboard

## 🔐 Default Login Credentials

### Admin Access
- **Username**: `admin`
- **Password**: `admin123`
- **Email**: `admin@wsei.pl`

### Test Student
- **Registration Number**: `WSEI20250001`
- **Email**: `john.smith@student.wsei.pl`
- **Password**: `john@123`

## 🛠️ Troubleshooting

### Build Errors
1. **Prisma Client**: Ensure `postinstall` script runs
2. **TypeScript**: Check for type errors with `npx tsc --noEmit`
3. **Environment Variables**: Verify all required variables are set

### Database Connection Issues
1. **Check DATABASE_URL**: Ensure it's correctly formatted
2. **Network Access**: Verify database allows connections from Vercel
3. **SSL**: Enable SSL for production databases

### Authentication Issues
1. **NEXTAUTH_SECRET**: Generate a new secure secret
2. **Session Storage**: Check if sessions are being stored correctly
3. **Password Hashing**: Verify bcrypt is working properly

## 📞 Support

For deployment issues:
1. Check Vercel deployment logs
2. Verify environment variables
3. Test database connectivity
4. Review application logs

## 🔄 Update Process

1. **Make changes** to your code
2. **Commit and push** to GitHub
3. **Vercel auto-deploys** from GitHub
4. **Database migrations** run automatically
5. **Test the deployment**

---

**Note**: Always test changes locally before deploying to production! 