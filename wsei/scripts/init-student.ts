#!/usr/bin/env tsx

import { PrismaClient } from '@prisma/client'
import { hashPassword, generateRegistrationNumber } from '../lib/auth'

const prisma = new PrismaClient()

async function initStudent() {
  try {
    const studentEmail = 'john.smith@student.wsei.pl'
    const studentPassword = 'student123'
    const registrationNo = 'WSEI20250001'

    // Check if student user already exists
    const existingStudent = await prisma.user.findFirst({
      where: {
        OR: [
          { username: registrationNo },
          { email: studentEmail }
        ]
      }
    })

    if (existingStudent) {
      console.log('Student user already exists')
      return
    }

    // Hash the student password
    const hashedPassword = await hashPassword(studentPassword)

    // Create student user and student record in a transaction
    const result = await prisma.$transaction(async (tx) => {
      // Create the user
      const user = await tx.user.create({
        data: {
          username: registrationNo,
          email: studentEmail,
          password: hashedPassword,
          role: 'STUDENT'
        }
      })

      // Create the student record
      const student = await tx.student.create({
        data: {
          registrationNo: registrationNo,
          firstName: 'John',
          lastName: 'Smith',
          dateOfBirth: new Date('1995-03-15'),
          courseOfStudy: 'Computer Science',
          semester: 3,
          email: studentEmail,
          phone: '+48 123 456 789',
          address: 'ul. Akademicka 1, 20-209 Lublin',
          enrollmentDate: new Date('2025-10-01'),
          status: 'ACTIVE',
          userId: user.id
        }
      })

      return { user, student }
    })

    console.log('Student user created successfully:', {
      id: result.user.id,
      username: result.user.username,
      email: result.user.email,
      role: result.user.role,
      studentId: result.student.id,
      registrationNo: result.student.registrationNo
    })

    console.log('\n📋 Test Student Login Credentials:')
    console.log('Registration Number:', registrationNo)
    console.log('Email:', studentEmail)
    console.log('Password:', studentPassword)

  } catch (error) {
    console.error('Error creating student user:', error)
  } finally {
    await prisma.$disconnect()
  }
}

initStudent() 