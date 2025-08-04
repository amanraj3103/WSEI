import { NextRequest, NextResponse } from 'next/server'
import { prisma } from '@/lib/db'
import { hashPassword, generateRegistrationNumber } from '@/lib/auth'

export async function POST(request: NextRequest) {
  try {
    const {
      email,
      password,
      firstName,
      lastName,
      dateOfBirth,
      courseOfStudy,
      semester
    } = await request.json()

    // Validate required fields
    if (!email || !password || !firstName || !lastName || !dateOfBirth || !courseOfStudy || !semester) {
      return NextResponse.json(
        { message: 'All fields are required' },
        { status: 400 }
      )
    }

    // Validate email format: first_name.last_name@student.wsei.pl
    const cleanFirstName = firstName.toLowerCase().replace(/[^a-z]/g, '')
    const cleanLastName = lastName.toLowerCase().replace(/[^a-z]/g, '')
    const expectedEmail = `${cleanFirstName}.${cleanLastName}@student.wsei.pl`
    
    if (email.toLowerCase() !== expectedEmail) {
      return NextResponse.json(
        { message: `Email must be in the format: ${expectedEmail}` },
        { status: 400 }
      )
    }

    // Check if user already exists (by email)
    const existingUserByEmail = await prisma.user.findFirst({
      where: {
        email: email.toLowerCase()
      }
    })

    if (existingUserByEmail) {
      return NextResponse.json(
        { message: 'Email already exists' },
        { status: 409 }
      )
    }

    // Check if user already exists (by name combination)
    const existingUserByName = await prisma.student.findFirst({
      where: {
        AND: [
          { firstName: firstName },
          { lastName: lastName }
        ]
      }
    })

    if (existingUserByName) {
      return NextResponse.json(
        { message: 'A student with this name already exists' },
        { status: 409 }
      )
    }

    // Generate unique registration number
    let registrationNo: string
    let isUnique = false
    let attempts = 0

    while (!isUnique && attempts < 10) {
      registrationNo = generateRegistrationNumber()
      const existingStudent = await prisma.student.findUnique({
        where: { registrationNo }
      })
      
      if (!existingStudent) {
        isUnique = true
      }
      attempts++
    }

    if (!isUnique) {
      return NextResponse.json(
        { message: 'Failed to generate unique registration number' },
        { status: 500 }
      )
    }

    // Hash password
    const hashedPassword = await hashPassword(password)

    // Create user and student in a transaction
    const result = await prisma.$transaction(async (tx) => {
      // Create user with registration number as username
      const user = await tx.user.create({
        data: {
          username: registrationNo!,
          email,
          password: hashedPassword,
          role: 'STUDENT'
        }
      })

      // Create student
      const student = await tx.student.create({
        data: {
          registrationNo: registrationNo!,
          firstName,
          lastName,
          dateOfBirth: new Date(dateOfBirth),
          courseOfStudy,
          semester: parseInt(semester),
          email,
          userId: user.id
        }
      })

      return { user, student }
    })

    return NextResponse.json({
      success: true,
      message: 'Registration successful',
      registrationNo: result.student.registrationNo
    })

  } catch (error) {
    console.error('Signup error:', error)
    return NextResponse.json(
      { message: 'Internal server error' },
      { status: 500 }
    )
  }
} 