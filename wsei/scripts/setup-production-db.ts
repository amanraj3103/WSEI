#!/usr/bin/env tsx

import { PrismaClient } from '@prisma/client'
import { hashPassword, generateRegistrationNumber } from '../lib/auth'

const prisma = new PrismaClient()

async function setupProductionDatabase() {
  try {
    console.log('🚀 Setting up production database...')

    // Generate Prisma client
    console.log('📦 Generating Prisma client...')
    await prisma.$connect()

    // Create admin user
    console.log('👤 Creating admin user...')
    const adminPassword = await hashPassword('admin123')
    
    const adminUser = await prisma.user.upsert({
      where: { email: 'admin@wsei.pl' },
      update: {},
      create: {
        email: 'admin@wsei.pl',
        username: 'admin',
        password: adminPassword,
        role: 'ADMIN'
      }
    })

    console.log('✅ Admin user created/updated:', {
      id: adminUser.id,
      username: adminUser.username,
      email: adminUser.email,
      role: adminUser.role
    })

    // Create a sample student for testing
    console.log('🎓 Creating sample student...')
    const studentPassword = await hashPassword('john@123')
    const registrationNo = generateRegistrationNumber()
    
    const studentUser = await prisma.user.upsert({
      where: { email: 'john.smith@student.wsei.pl' },
      update: {},
      create: {
        email: 'john.smith@student.wsei.pl',
        username: registrationNo,
        password: studentPassword,
        role: 'STUDENT'
      }
    })

    const student = await prisma.student.upsert({
      where: { userId: studentUser.id },
      update: {},
      create: {
        registrationNo: registrationNo,
        firstName: 'John',
        lastName: 'Smith',
        dateOfBirth: new Date('1995-03-15'),
        courseOfStudy: 'Computer Science',
        semester: 3,
        email: 'john.smith@student.wsei.pl',
        phone: '+48 123 456 789',
        address: 'ul. Akademicka 1, 20-209 Lublin',
        enrollmentDate: new Date('2025-10-01'),
        status: 'ACTIVE',
        userId: studentUser.id
      }
    })

    console.log('✅ Sample student created/updated:', {
      id: student.id,
      registrationNo: student.registrationNo,
      name: `${student.firstName} ${student.lastName}`,
      email: student.email
    })

    console.log('\n🎉 Production database setup completed!')
    console.log('\n📋 Login Credentials:')
    console.log('👤 Admin: admin / admin123')
    console.log('🎓 Student: WSEI20250001 / john@123')
    console.log('📧 Student Email: john.smith@student.wsei.pl')

  } catch (error) {
    console.error('❌ Error setting up production database:', error)
    process.exit(1)
  } finally {
    await prisma.$disconnect()
  }
}

setupProductionDatabase() 