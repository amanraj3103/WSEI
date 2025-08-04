#!/usr/bin/env tsx

import { PrismaClient } from '@prisma/client'
import { hashPassword } from '../lib/auth'

const prisma = new PrismaClient()

async function updateStudentPasswords() {
  try {
    console.log('🔐 Updating student passwords to new format...')

    // Get all students
    const students = await prisma.student.findMany({
      include: {
        user: true
      }
    })

    console.log(`Found ${students.length} students to update`)

    let updatedCount = 0
    let errorCount = 0

    for (const student of students) {
      try {
        // Generate new password based on first name
        const cleanFirstName = student.firstName.toLowerCase().replace(/[^a-z]/g, '')
        const newPassword = `${cleanFirstName}@123`
        
        // Hash the new password
        const hashedPassword = await hashPassword(newPassword)

        // Update the user's password
        await prisma.user.update({
          where: { id: student.user.id },
          data: { password: hashedPassword }
        })

        console.log(`✅ Updated ${student.firstName} ${student.lastName}: ${newPassword}`)
        updatedCount++

      } catch (error) {
        console.error(`❌ Error updating ${student.firstName} ${student.lastName}:`, error)
        errorCount++
      }
    }

    console.log('\n📊 Update Summary:')
    console.log(`✅ Successfully updated: ${updatedCount} students`)
    console.log(`❌ Errors: ${errorCount} students`)
    console.log(`📝 Total processed: ${students.length} students`)

    if (updatedCount > 0) {
      console.log('\n🔑 New Password Format: firstname@123')
      console.log('📧 Email Format: firstname.lastname@student.wsei.pl')
      console.log('\n💡 Students can now login with their registration number or email and the new password format.')
    }

  } catch (error) {
    console.error('❌ Error updating passwords:', error)
  } finally {
    await prisma.$disconnect()
  }
}

updateStudentPasswords() 