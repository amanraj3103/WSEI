import { NextRequest, NextResponse } from 'next/server'
import { prisma } from '@/lib/db'

export async function GET(request: NextRequest) {
  try {
    const students = await prisma.student.findMany({
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

    return NextResponse.json({
      success: true,
      students: students.map(student => ({
        id: student.id,
        registrationNo: student.registrationNo,
        firstName: student.firstName,
        lastName: student.lastName,
        courseOfStudy: student.courseOfStudy,
        semester: student.semester,
        email: student.email,
        phone: student.phone,
        address: student.address,
        enrollmentDate: student.enrollmentDate,
        status: student.status,
        user: student.user
      }))
    })

  } catch (error) {
    console.error('Error fetching students:', error)
    return NextResponse.json(
      { message: 'Internal server error' },
      { status: 500 }
    )
  }
} 