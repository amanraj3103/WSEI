#!/usr/bin/env tsx

import { PrismaClient } from '@prisma/client'

const prisma = new PrismaClient()

async function checkDatabase() {
  try {
    console.log('🔍 Checking production database...')
    
    // Check users
    const users = await prisma.user.findMany({
      include: {
        student: true
      }
    })
    
    console.log('\n👥 Users found:', users.length)
    users.forEach(user => {
      console.log(`- ${user.username} (${user.email}) - Role: ${user.role}`)
      if (user.student) {
        console.log(`  └─ Student: ${user.student.firstName} ${user.student.lastName}`)
      }
    })
    
    // Check students
    const students = await prisma.student.findMany({
      include: {
        user: true
      }
    })
    
    console.log('\n🎓 Students found:', students.length)
    students.forEach(student => {
      console.log(`- ${student.registrationNo}: ${student.firstName} ${student.lastName}`)
      console.log(`  └─ Email: ${student.email}, Course: ${student.courseOfStudy}, Semester: ${student.semester}`)
    })
    
    // Test the exact query from the API
    console.log('\n🔍 Testing API query...')
    const apiStudents = await prisma.student.findMany({
      include: {
        user: {
          select: {
            id: true,
            username: true,
            email: true,
            role: true
          }
        }
      },
      orderBy: {
        registrationNo: 'asc'
      }
    })
    
    console.log('API query returned:', apiStudents.length, 'students')
    
  } catch (error) {
    console.error('❌ Error checking database:', error)
  } finally {
    await prisma.$disconnect()
  }
}

checkDatabase() 