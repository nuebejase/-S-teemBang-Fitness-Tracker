<script setup lang="ts">
import Card from '@/components/ui/Card.vue'
import { MapPin, Phone, Mail, Clock } from 'lucide-vue-next'
</script>

<template>
  <div class="min-h-screen bg-gradient-to-b from-pink-50 to-white">
    <section class="bg-gradient-to-r from-pink-500 to-pink-600 text-white py-20">
      <div class="container mx-auto px-4 text-center">
        <h1 class="text-5xl font-bold mb-4">About FrinStore</h1>
        <p class="text-xl text-pink-100 max-w-2xl mx-auto">
          Your local ice cream shop dedicated to bringing happiness one scoop at a time
        </p>
      </div>
    </section>

    <section class="py-16">
      <div class="container mx-auto px-4">
        <div class="max-w-3xl mx-auto">
          <Card class="p-8 border-pink-200">
            <h2 class="text-3xl font-bold mb-6 text-center">Our Story</h2>
            <div class="space-y-4 text-gray-700">
              <p>
                Founded in 2020, FrinStore began with a simple mission: to create the most delicious
                and memorable ice cream experience for our community. What started as a small local
                shop has grown into a beloved destination for ice cream lovers of all ages.
              </p>
              <p>
                We believe that ice cream is more than just a dessert—it's a moment of joy, a memory
                in the making, and a treat that brings people together. That's why we use only the
                finest ingredients and craft each flavor with care and passion.
              </p>
              <p>
                Today, we're proud to offer our handcrafted ice cream through our convenient online
                marketplace, bringing our delicious flavors directly to your doorstep.
              </p>
            </div>
          </Card>
        </div>
      </div>
    </section>

    <section class="py-16 bg-white">
      <div class="container mx-auto px-4">
        <h2 class="text-4xl font-bold text-center mb-12">Get In Touch</h2>
        <div class="grid md:grid-cols-2 lg:grid-cols-4 gap-6 max-w-5xl mx-auto">
          <Card class="p-6 text-center border-pink-200 hover:shadow-lg transition-shadow">
            <div class="w-16 h-16 bg-pink-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <MapPin class="w-8 h-8 text-pink-600" />
            </div>
            <h3 class="font-bold mb-2">Address</h3>
            <p class="text-gray-600 text-sm">
              123 Sweet Street<br />
              Manila, Philippines
            </p>
          </Card>
          <Card class="p-6 text-center border-pink-200 hover:shadow-lg transition-shadow">
            <div class="w-16 h-16 bg-pink-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <Phone class="w-8 h-8 text-pink-600" />
            </div>
            <h3 class="font-bold mb-2">Phone</h3>
            <p class="text-gray-600 text-sm">
              (123) 456-7890<br />
              (123) 456-7891
            </p>
          </Card>
          <Card class="p-6 text-center border-pink-200 hover:shadow-lg transition-shadow">
            <div class="w-16 h-16 bg-pink-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <Mail class="w-8 h-8 text-pink-600" />
            </div>
            <h3 class="font-bold mb-2">Email</h3>
            <p class="text-gray-600 text-sm">
              info@frinstore.com<br />
              support@frinstore.com
            </p>
          </Card>
          <Card class="p-6 text-center border-pink-200 hover:shadow-lg transition-shadow">
            <div class="w-16 h-16 bg-pink-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <Clock class="w-8 h-8 text-pink-600" />
            </div>
            <h3 class="font-bold mb-2">Hours</h3>
            <p class="text-gray-600 text-sm">
              Mon-Sun<br />
              9:00 AM - 9:00 PM
            </p>
          </Card>
        </div>
      </div>
    </section>

    <section class="py-16">
      <div class="container mx-auto px-4">
        <h2 class="text-4xl font-bold text-center mb-12">Our Values</h2>
        <div class="grid md:grid-cols-3 gap-8 max-w-5xl mx-auto">
          <Card class="p-6 border-pink-200">
            <div class="text-4xl mb-4 text-center" aria-hidden="true">🌟</div>
            <h3 class="font-bold text-xl mb-3 text-center">Quality First</h3>
            <p class="text-gray-600 text-center">
              We use only premium ingredients to ensure every scoop is perfect
            </p>
          </Card>
          <Card class="p-6 border-pink-200">
            <div class="text-4xl mb-4 text-center" aria-hidden="true">❤️</div>
            <h3 class="font-bold text-xl mb-3 text-center">Made with Love</h3>
            <p class="text-gray-600 text-center">
              Every product is crafted with passion and dedication
            </p>
          </Card>
          <Card class="p-6 border-pink-200">
            <div class="text-4xl mb-4 text-center" aria-hidden="true">🌍</div>
            <h3 class="font-bold text-xl mb-3 text-center">Community</h3>
            <p class="text-gray-600 text-center">
              Supporting our local community with every order
            </p>
          </Card>
        </div>
      </div>
    </section>
  </div>
</template>
