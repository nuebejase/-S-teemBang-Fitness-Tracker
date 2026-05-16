<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import Button from '@/components/ui/Button.vue'
import Card from '@/components/ui/Card.vue'
import { useAppStore } from '@/stores/appStore'
import type { Product } from '@/types/domain'
import { Plus, Edit, Trash2, Search, Package, X } from 'lucide-vue-next'
import { toast } from 'vue-sonner'

const appStore = useAppStore()

const DEFAULT_IMAGE =
  'https://images.unsplash.com/photo-1563805042-7684c019e1cb?w=400'

onMounted(() => {
  void appStore.fetchProducts()
})

const searchQuery = ref('')
const selectedCategory = ref('all')
const showProductModal = ref(false)
const editingProduct = ref<Product | null>(null)
const deleteTarget = ref<Product | null>(null)

const formData = ref({
  name: '',
  description: '',
  price: 0,
  image: '',
  category: '',
  flavor: '',
  stock: 0,
})

const categories = computed(() => ['all', ...new Set(appStore.products.map((p) => p.category))])

const filteredProducts = computed(() => {
  let list = appStore.products
  if (searchQuery.value) {
    const q = searchQuery.value.toLowerCase()
    list = list.filter(
      (p) =>
        p.name.toLowerCase().includes(q) || p.description.toLowerCase().includes(q),
    )
  }
  if (selectedCategory.value !== 'all') {
    list = list.filter((p) => p.category === selectedCategory.value)
  }
  return list
})

const resetFormFields = () => {
  formData.value = {
    name: '',
    description: '',
    price: 0,
    image: '',
    category: '',
    flavor: '',
    stock: 0,
  }
  editingProduct.value = null
}

const closeProductModal = () => {
  showProductModal.value = false
  resetFormFields()
}

const openAddProduct = () => {
  resetFormFields()
  showProductModal.value = true
}

const handleSaveProduct = async () => {
  const name = formData.value.name.trim()
  const description = formData.value.description.trim()
  const category = formData.value.category.trim()
  const flavor = formData.value.flavor.trim()
  const price = Number(formData.value.price)
  const stock = Math.max(0, Math.floor(Number(formData.value.stock)) || 0)
  const image = (formData.value.image.trim() || DEFAULT_IMAGE).trim()

  if (!name || !description || !category || !flavor) {
    toast.error('Please fill in all required fields')
    return
  }
  if (!Number.isFinite(price) || price <= 0) {
    toast.error('Price must be a number greater than zero')
    return
  }

  const payload = {
    name,
    description,
    price,
    image,
    category,
    flavor,
    stock,
  }

  try {
    if (editingProduct.value) {
      await appStore.updateProduct(editingProduct.value.id, payload)
      toast.success('Product updated successfully!')
    } else {
      await appStore.addProduct(payload)
      toast.success('Product added successfully!')
    }
    closeProductModal()
  } catch (e) {
    toast.error(e instanceof Error ? e.message : 'Could not save product')
  }
}

const handleEdit = (product: Product) => {
  editingProduct.value = product
  formData.value = {
    name: product.name,
    description: product.description,
    price: product.price,
    image: product.image,
    category: product.category,
    flavor: product.flavor,
    stock: product.stock,
  }
  showProductModal.value = true
}

const openDeleteModal = (product: Product) => {
  deleteTarget.value = product
}

const closeDeleteModal = () => {
  deleteTarget.value = null
}

const confirmDelete = async () => {
  if (!deleteTarget.value) return
  const id = deleteTarget.value.id
  try {
    await appStore.deleteProduct(id)
    toast.success('Product deleted successfully!')
    closeDeleteModal()
  } catch (e) {
    toast.error(e instanceof Error ? e.message : 'Could not delete product')
  }
}

const getStockStatus = (stock: number) => {
  if (stock === 0) return { text: 'Out of Stock', color: 'text-red-600 bg-red-100' }
  if (stock < 10) return { text: 'Low Stock', color: 'text-orange-600 bg-orange-100' }
  return { text: 'In Stock', color: 'text-green-600 bg-green-100' }
}
</script>

<template>
  <div class="container mx-auto px-4 py-8">
    <div class="flex items-center justify-between mb-8">
      <div>
        <h1 class="text-4xl font-bold text-gray-900 mb-2">Manage Products</h1>
        <p class="text-gray-600">{{ filteredProducts.length }} products</p>
      </div>
      <Button
        type="button"
        class="bg-gradient-to-r from-pink-500 to-pink-600 hover:from-pink-600 hover:to-pink-700"
        @click="openAddProduct"
      >
        <Plus class="w-4 h-4 mr-2" />
        Add Product
      </Button>
    </div>

    <div class="bg-white rounded-lg shadow-sm border border-pink-100 p-6 mb-8">
      <div class="grid md:grid-cols-2 gap-4">
        <div class="relative">
          <Search class="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400 w-4 h-4" />
          <input
            v-model="searchQuery"
            type="text"
            placeholder="Search products..."
            class="w-full pl-10 pr-4 py-2 border border-pink-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-pink-500"
          />
        </div>
        <select
          v-model="selectedCategory"
          class="w-full px-4 py-2 border border-pink-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-pink-500"
        >
          <option value="all">All Categories</option>
          <option v-for="category in categories.filter((c) => c !== 'all')" :key="category" :value="category">
            {{ category }}
          </option>
        </select>
      </div>
    </div>

    <Teleport to="body">
      <div
        v-if="showProductModal"
        class="fixed inset-0 z-[100] flex items-center justify-center p-4 bg-black/50"
        role="dialog"
        aria-modal="true"
        :aria-labelledby="editingProduct ? 'edit-product-title' : 'add-product-title'"
      >
        <div class="bg-white rounded-xl shadow-xl max-w-3xl w-full max-h-[90vh] overflow-y-auto p-6 relative">
          <button
            type="button"
            class="absolute top-4 right-4 p-2 rounded-full text-gray-500 hover:bg-gray-100"
            aria-label="Close"
            @click="closeProductModal"
          >
            <X class="w-5 h-5" />
          </button>
          <h3 :id="editingProduct ? 'edit-product-title' : 'add-product-title'" class="text-xl font-semibold mb-6 pr-10">
            {{ editingProduct ? 'Edit Product' : 'Add New Product' }}
          </h3>
          <div class="grid md:grid-cols-2 gap-6">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Product Name *</label>
              <input
                v-model="formData.name"
                type="text"
                required
                class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-pink-500 focus:border-transparent"
              />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Price *</label>
              <input
                v-model.number="formData.price"
                type="number"
                min="0"
                step="1"
                class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-pink-500 focus:border-transparent"
              />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Category *</label>
              <select
                v-model="formData.category"
                required
                class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-pink-500 focus:border-transparent"
              >
                <option value="">Select category</option>
                <option value="Classic">Classic</option>
                <option value="Premium">Premium</option>
                <option value="Fruity">Fruity</option>
                <option value="Special">Special</option>
              </select>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Flavor *</label>
              <input
                v-model="formData.flavor"
                type="text"
                class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-pink-500 focus:border-transparent"
              />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Stock Quantity</label>
              <input
                v-model.number="formData.stock"
                type="number"
                min="0"
                class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-pink-500 focus:border-transparent"
              />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Image URL</label>
              <input
                v-model="formData.image"
                type="url"
                placeholder="Leave blank for default photo"
                class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-pink-500 focus:border-transparent"
              />
            </div>
            <div class="md:col-span-2">
              <label class="block text-sm font-medium text-gray-700 mb-2">Description *</label>
              <textarea
                v-model="formData.description"
                rows="3"
                class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-pink-500 focus:border-transparent"
              />
            </div>
          </div>
          <div class="flex flex-wrap gap-3 mt-6">
            <Button
              type="button"
              class="bg-gradient-to-r from-pink-500 to-pink-600 hover:from-pink-600 hover:to-pink-700"
              @click="handleSaveProduct"
            >
              {{ editingProduct ? 'Update Product' : 'Add Product' }}
            </Button>
            <Button type="button" variant="outline" @click="closeProductModal">Cancel</Button>
          </div>
        </div>
      </div>
    </Teleport>

    <Teleport to="body">
      <div
        v-if="deleteTarget"
        class="fixed inset-0 z-[100] flex items-center justify-center p-4 bg-black/50"
        role="dialog"
        aria-modal="true"
        aria-labelledby="delete-product-title"
      >
        <div class="bg-white rounded-xl shadow-xl max-w-md w-full p-6 space-y-4">
          <h2 id="delete-product-title" class="text-lg font-bold text-gray-900">Delete product?</h2>
          <p class="text-gray-600 text-sm">
            This will remove <strong>{{ deleteTarget.name }}</strong> from the catalog. Orders that already reference it
            keep their line items.
          </p>
          <div class="flex justify-end gap-3 pt-2">
            <Button type="button" variant="outline" @click="closeDeleteModal">Cancel</Button>
            <Button type="button" class="bg-red-600 hover:bg-red-700 text-white" @click="confirmDelete">Delete</Button>
          </div>
        </div>
      </div>
    </Teleport>

    <div v-if="filteredProducts.length > 0" class="grid md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
      <Card
        v-for="product in filteredProducts"
        :key="product.id"
        class="overflow-hidden border-pink-200 hover:shadow-lg transition-shadow"
      >
        <div class="relative h-48 overflow-hidden">
          <img :src="product.image" :alt="product.name" class="w-full h-full object-cover" />
          <div class="absolute top-2 right-2 bg-pink-500 text-white px-2 py-1 rounded-full text-sm">
            ₱{{ product.price }}
          </div>
          <div class="absolute top-2 left-2">
            <span :class="`px-2 py-1 rounded-full text-xs font-medium ${getStockStatus(product.stock).color}`">
              {{ getStockStatus(product.stock).text }}
            </span>
          </div>
        </div>
        <div class="p-4">
          <h3 class="font-bold text-lg mb-1">{{ product.name }}</h3>
          <p class="text-gray-600 text-sm mb-3 line-clamp-2">{{ product.description }}</p>
          <div class="flex items-center justify-between mb-3">
            <span class="text-sm text-pink-600 font-medium">{{ product.category }}</span>
            <span class="text-sm text-gray-500">{{ product.flavor }}</span>
          </div>
          <div class="flex items-center justify-between">
            <span class="text-xs text-gray-500">Stock: {{ product.stock }}</span>
            <div class="flex space-x-2">
              <Button type="button" variant="outline" size="sm" @click="handleEdit(product)">
                <Edit class="w-3 h-3" />
              </Button>
              <Button
                type="button"
                variant="ghost"
                size="sm"
                class="text-red-500 hover:text-red-700"
                @click="openDeleteModal(product)"
              >
                <Trash2 class="w-3 h-3" />
              </Button>
            </div>
          </div>
        </div>
      </Card>
    </div>

    <div v-else class="text-center py-12">
      <Package class="w-16 h-16 mx-auto text-gray-400 mb-4" />
      <h3 class="text-xl font-semibold text-gray-700 mb-2">No products found</h3>
      <p class="text-gray-600 mb-4">Try adjusting your filters or add a new product</p>
      <Button
        type="button"
        class="bg-gradient-to-r from-pink-500 to-pink-600 hover:from-pink-600 hover:to-pink-700"
        @click="openAddProduct"
      >
        <Plus class="w-4 h-4 mr-2" />
        Add Your First Product
      </Button>
    </div>
  </div>
</template>
