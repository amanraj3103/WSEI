import { PrismaClient } from '@prisma/client'
import { hashPassword } from '../lib/auth'

const prisma = new PrismaClient()

async function initAdmin() {
  try {
    const adminUsername = process.env.ADMIN_USERNAME || 'admin'
    const adminPassword = process.env.ADMIN_PASSWORD || 'admin123'
    const adminEmail = process.env.ADMIN_EMAIL || 'admin@wsei.pl'

    // Check if admin user already exists
    const existingAdmin = await prisma.user.findFirst({
      where: {
        OR: [
          { username: adminUsername },
          { email: adminEmail }
        ]
      }
    })

    if (existingAdmin) {
      console.log('Admin user already exists')
      return
    }

    // Hash the admin password
    const hashedPassword = await hashPassword(adminPassword)

    // Create admin user
    const adminUser = await prisma.user.create({
      data: {
        username: adminUsername,
        email: adminEmail,
        password: hashedPassword,
        role: 'ADMIN'
      }
    })

    console.log('Admin user created successfully:', {
      id: adminUser.id,
      username: adminUser.username,
      email: adminUser.email,
      role: adminUser.role
    })

  } catch (error) {
    console.error('Error creating admin user:', error)
  } finally {
    await prisma.$disconnect()
  }
}

initAdmin() 