import { NextRequest, NextResponse } from 'next/server'
import { prisma } from '@/lib/db'

export async function GET(request: NextRequest) {
  try {
    // Get the user ID from query params
    const { searchParams } = new URL(request.url)
    const userId = searchParams.get('userId')
    
    if (!userId) {
      return NextResponse.json(
        { message: 'User ID is required' },
        { status: 400 }
      )
    }

    const whereClause = { userId: userId }

    const student = await prisma.student.findFirst({
      where: whereClause,
      include: {
        user: {
          select: {
            id: true,
            username: true,
            email: true,
            role: true
          }
        }
      }
    })

    if (!student) {
      return NextResponse.json(
        { message: 'Student not found' },
        { status: 404 }
      )
    }

    return NextResponse.json({
      success: true,
      student: {
        id: student.id,
        registrationNo: student.registrationNo,
        firstName: student.firstName,
        lastName: student.lastName,
        dateOfBirth: student.dateOfBirth,
        courseOfStudy: student.courseOfStudy,
        semester: student.semester,
        email: student.email,
        phone: student.phone,
        address: student.address,
        enrollmentDate: student.enrollmentDate,
        status: student.status,
        user: student.user
      }
    })

  } catch (error) {
    console.error('Error fetching student profile:', error)
    return NextResponse.json(
      { message: 'Internal server error' },
      { status: 500 }
    )
  }
} 