<template>
  <div class="app">
    <i
      :class="theme === 'light' ? 'fas fa-moon' : 'fas fa-sun'"
      @click="toggleTheme"
      class="theme-toggle"
      title="Toggle Theme"
    ></i>
    <h1>IBM News</h1>
    <div class="controls">
      <label for="news-size">Number of news items:</label>
      <input type="number" id="news-size" v-model="newsSize" min="10" max="100" step="10">
      <button @click="fetchNews">Fetch News</button>
    </div>
    <!-- Loading spinner -->
    <div v-if="loading" class="spinner">
      <i class="fas fa-hourglass-half fa-spin" style="font-size: 24px;"></i>
    </div>
    <div class="news-container" v-else>
      <NewsCard v-for="item in newsItems" :key="item.url" :news="item" />
    </div>
  </div>
</template>

<script>
import NewsCard from './components/NewsCard.vue';

export default {
  components: {
    NewsCard
  },
  data() {
    return {
      newsSize: 10,
      newsItems: [],
      theme: 'light', // Default theme
      loading: false  // Loading state
    };
  },
  watch: {
    theme(newTheme) {
      document.body.className = newTheme; // Apply theme to the body element
    }
  },
  mounted() {
    document.body.className = this.theme; // Set initial theme on mount
  },
  methods: {
    fetchNews() {
      this.loading = true; // Start loading
      fetch(`http://127.0.0.1:5000/news?size=${this.newsSize}`)
        .then(response => response.json())
        .then(data => {
          this.newsItems = data;
        })
        .catch(error => console.error('Error fetching news:', error))
        .finally(() => {
          this.loading = false; // End loading
        });
    },
    toggleTheme() {
      this.theme = this.theme === 'light' ? 'dark' : 'light';
    }
  }
}
</script>

<style>
body.light {
  background-color: #ffffff;
  color: #2c3e50;
}

body.dark {
  background-color: #2c3e50;
  color: #ffffff;
}

.app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  text-align: center;
  margin-top: 20px; /* Reduce top margin */
  transition: background-color 0.3s, color 0.3s;
  position: relative;
}

.theme-toggle {
  position: absolute;
  top: 10px;
  right: 10px;
  cursor: pointer;
  font-size: 24px;
}

.controls {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 20px; /* Add space between controls */
  margin-bottom: 20px; /* Add space below controls */
}

.news-container {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
}

.news-card {
  border: 1px solid #ccc;
  border-radius: 8px;
  overflow: hidden;
  margin: 10px;
  display: flex;
  flex-direction: column;
  max-width: 300px;
  transition: background-color 0.3s, color 0.3s;
}

.news-card img {
  width: 100%;
  height: auto;
}

.news-card .news-content {
  padding: 10px;
}

body.light .news-card {
  background-color: #f9f9f9;
  color: #2c3e50;
}

body.dark .news-card {
  background-color: #3e3e3e;
  color: #ffffff;
}

.spinner {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100px; /* Adjust height as needed */
  margin-top: 20px;
}
</style>
