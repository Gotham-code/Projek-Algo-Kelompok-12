"""
Unit tests for SISTA - Sistem Rekomendasi Irigasi dan Stok Agroindustri
"""

import unittest
from sista import (
    calculate_irrigation,
    CROP_WATER_REQUIREMENTS,
    SOIL_FACTORS,
    WEATHER_FACTORS,
    stock_data,
    generate_stock_id,
    reset_stock_id_counter
)


class TestIrrigationCalculation(unittest.TestCase):
    """Test cases for irrigation calculation."""
    
    def test_basic_irrigation_calculation(self):
        """Test basic irrigation calculation for padi on lempung soil, berawan weather."""
        result = calculate_irrigation("padi", "lempung", "berawan", 100)
        
        # Padi base: 8, lempung factor: 1.0, berawan factor: 1.0
        # water_per_sqm = 8 * 1.0 * 1.0 = 8
        # total_water = 8 * 100 = 800
        self.assertEqual(result['water_per_sqm'], 8.0)
        self.assertEqual(result['total_water'], 800.0)
        self.assertEqual(result['priority'], 'Normal')
    
    def test_irrigation_with_sandy_soil(self):
        """Test irrigation calculation with berpasir soil (higher factor)."""
        result = calculate_irrigation("jagung", "berpasir", "berawan", 100)
        
        # Jagung base: 5, berpasir factor: 1.3, berawan factor: 1.0
        # water_per_sqm = 5 * 1.3 * 1.0 = 6.5
        expected = 5 * 1.3 * 1.0
        self.assertAlmostEqual(result['water_per_sqm'], expected)
    
    def test_irrigation_sunny_weather(self):
        """Test irrigation calculation with cerah weather (higher evaporation)."""
        result = calculate_irrigation("cabai", "lempung", "cerah", 100)
        
        # Cabai base: 6, lempung factor: 1.0, cerah factor: 1.2
        # water_per_sqm = 6 * 1.0 * 1.2 = 7.2
        expected = 6 * 1.0 * 1.2
        self.assertAlmostEqual(result['water_per_sqm'], expected)
        self.assertEqual(result['priority'], 'Tinggi')
    
    def test_irrigation_heavy_rain(self):
        """Test irrigation calculation with hujan_deras weather (minimal irrigation)."""
        result = calculate_irrigation("tomat", "lempung", "hujan_deras", 100)
        
        # Tomat base: 5, lempung factor: 1.0, hujan_deras factor: 0.2
        # water_per_sqm = 5 * 1.0 * 0.2 = 1.0
        expected = 5 * 1.0 * 0.2
        self.assertAlmostEqual(result['water_per_sqm'], expected)
        self.assertEqual(result['priority'], 'Rendah')
    
    def test_irrigation_light_rain(self):
        """Test irrigation calculation with hujan_ringan weather."""
        result = calculate_irrigation("kedelai", "lempung", "hujan_ringan", 100)
        
        # Kedelai base: 4, lempung factor: 1.0, hujan_ringan factor: 0.5
        expected = 4 * 1.0 * 0.5
        self.assertAlmostEqual(result['water_per_sqm'], expected)
        self.assertEqual(result['priority'], 'Sedang')
    
    def test_irrigation_total_water_calculation(self):
        """Test that total water is correctly calculated from area."""
        result = calculate_irrigation("tebu", "gambut", "berawan", 500)
        
        # Tebu base: 7, gambut factor: 0.9, berawan factor: 1.0
        # water_per_sqm = 7 * 0.9 * 1.0 = 6.3
        # total_water = 6.3 * 500 = 3150
        expected_per_sqm = 7 * 0.9 * 1.0
        expected_total = expected_per_sqm * 500
        
        self.assertAlmostEqual(result['water_per_sqm'], expected_per_sqm)
        self.assertAlmostEqual(result['total_water'], expected_total)
    
    def test_irrigation_result_contains_required_fields(self):
        """Test that result contains all required fields."""
        result = calculate_irrigation("padi", "lempung", "cerah", 100)
        
        required_fields = [
            'water_per_sqm', 'total_water', 'recommendation', 
            'priority', 'crop_name', 'soil_name', 'weather_name'
        ]
        
        for field in required_fields:
            self.assertIn(field, result)


class TestStockManagement(unittest.TestCase):
    """Test cases for stock management."""
    
    def setUp(self):
        """Clear stock data before each test."""
        stock_data.clear()
        reset_stock_id_counter()
    
    def test_generate_stock_id(self):
        """Test stock ID generation."""
        id1 = generate_stock_id()
        id2 = generate_stock_id()
        id3 = generate_stock_id()
        
        self.assertEqual(id1, "STK0001")
        self.assertEqual(id2, "STK0002")
        self.assertEqual(id3, "STK0003")
    
    def test_stock_data_is_list(self):
        """Test that stock_data is a list."""
        self.assertIsInstance(stock_data, list)
    
    def test_add_stock_manually(self):
        """Test adding stock item manually to stock_data."""
        stock_item = {
            "id": generate_stock_id(),
            "name": "Pupuk Urea",
            "category": "Pupuk",
            "quantity": 100,
            "unit": "karung",
            "price": 150000,
            "date_added": "01/01/2024 10:00:00"
        }
        
        stock_data.append(stock_item)
        
        self.assertEqual(len(stock_data), 1)
        self.assertEqual(stock_data[0]['name'], "Pupuk Urea")
        self.assertEqual(stock_data[0]['quantity'], 100)
    
    def test_update_stock_quantity(self):
        """Test updating stock quantity."""
        stock_item = {
            "id": generate_stock_id(),
            "name": "Pestisida",
            "category": "Pestisida",
            "quantity": 50,
            "unit": "liter",
            "price": 75000,
            "date_added": "01/01/2024 10:00:00"
        }
        
        stock_data.append(stock_item)
        
        # Add stock
        stock_data[0]['quantity'] += 25
        self.assertEqual(stock_data[0]['quantity'], 75)
        
        # Remove stock
        stock_data[0]['quantity'] -= 10
        self.assertEqual(stock_data[0]['quantity'], 65)
    
    def test_delete_stock(self):
        """Test deleting stock item."""
        stock_item = {
            "id": generate_stock_id(),
            "name": "Benih Jagung",
            "category": "Benih",
            "quantity": 20,
            "unit": "kg",
            "price": 50000,
            "date_added": "01/01/2024 10:00:00"
        }
        
        stock_data.append(stock_item)
        self.assertEqual(len(stock_data), 1)
        
        stock_data.pop(0)
        self.assertEqual(len(stock_data), 0)
    
    def test_search_stock_by_name(self):
        """Test searching stock by name."""
        items = [
            {"id": "STK0001", "name": "Pupuk Urea", "category": "Pupuk", 
             "quantity": 100, "unit": "karung", "price": 150000},
            {"id": "STK0002", "name": "Pupuk NPK", "category": "Pupuk", 
             "quantity": 50, "unit": "karung", "price": 200000},
            {"id": "STK0003", "name": "Pestisida", "category": "Pestisida", 
             "quantity": 30, "unit": "liter", "price": 75000},
        ]
        
        stock_data.extend(items)
        
        # Search for "pupuk"
        keyword = "pupuk"
        results = [item for item in stock_data 
                   if keyword in item['name'].lower() or keyword in item['category'].lower()]
        
        self.assertEqual(len(results), 2)
    
    def test_low_stock_alert(self):
        """Test low stock detection."""
        items = [
            {"id": "STK0001", "name": "Item A", "category": "Cat A", 
             "quantity": 5, "unit": "pcs", "price": 1000},
            {"id": "STK0002", "name": "Item B", "category": "Cat B", 
             "quantity": 50, "unit": "pcs", "price": 2000},
            {"id": "STK0003", "name": "Item C", "category": "Cat C", 
             "quantity": 8, "unit": "pcs", "price": 3000},
        ]
        
        stock_data.extend(items)
        
        threshold = 10
        low_items = [item for item in stock_data if item['quantity'] <= threshold]
        
        self.assertEqual(len(low_items), 2)


class TestDataConstants(unittest.TestCase):
    """Test cases for data constants."""
    
    def test_crop_water_requirements_not_empty(self):
        """Test that CROP_WATER_REQUIREMENTS is not empty."""
        self.assertGreater(len(CROP_WATER_REQUIREMENTS), 0)
    
    def test_soil_factors_not_empty(self):
        """Test that SOIL_FACTORS is not empty."""
        self.assertGreater(len(SOIL_FACTORS), 0)
    
    def test_weather_factors_not_empty(self):
        """Test that WEATHER_FACTORS is not empty."""
        self.assertGreater(len(WEATHER_FACTORS), 0)
    
    def test_crop_has_required_fields(self):
        """Test that each crop has required fields."""
        for key, data in CROP_WATER_REQUIREMENTS.items():
            self.assertIn('base', data)
            self.assertIn('name', data)
            self.assertIn('kategori', data)
            self.assertGreater(data['base'], 0)
    
    def test_soil_has_required_fields(self):
        """Test that each soil type has required fields."""
        for key, data in SOIL_FACTORS.items():
            self.assertIn('factor', data)
            self.assertIn('name', data)
            self.assertIn('desc', data)
            self.assertGreater(data['factor'], 0)
    
    def test_weather_has_required_fields(self):
        """Test that each weather type has required fields."""
        for key, data in WEATHER_FACTORS.items():
            self.assertIn('factor', data)
            self.assertIn('name', data)
            self.assertIn('desc', data)
            self.assertGreater(data['factor'], 0)


if __name__ == '__main__':
    unittest.main()
