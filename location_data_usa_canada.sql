-- =====================================================
-- LOCATION MANAGEMENT - USA & CANADA FOCUS
-- =====================================================

-- Clear existing location data (optional - remove if you want to keep existing data)
-- DELETE FROM cities WHERE id > 0;
-- DELETE FROM states WHERE id > 0;
-- DELETE FROM countries WHERE id > 0;

-- =====================================================
-- 1. COUNTRIES (USA & CANADA)
-- =====================================================

INSERT INTO countries (name, code_alpha2, code_alpha3, numeric_code, currency_code, phone_code, timezone_primary, sort_order, is_active, created_at) VALUES
('United States', 'US', 'USA', '840', 'USD', '+1', 'America/New_York', 1, TRUE, NOW()),
('Canada', 'CA', 'CAN', '124', 'CAD', '+1', 'America/Toronto', 2, TRUE, NOW());

-- =====================================================
-- 2. STATES/PROVINCES - UNITED STATES
-- =====================================================

INSERT INTO states (name, code, country_id, timezone_primary, sort_order, is_active, created_at) 
SELECT 'Alabama', 'AL', id, 'America/Chicago', 1, TRUE, NOW() FROM countries WHERE code_alpha2 = 'US';

INSERT INTO states (name, code, country_id, timezone_primary, sort_order, is_active, created_at) 
SELECT 'Alaska', 'AK', id, 'America/Anchorage', 2, TRUE, NOW() FROM countries WHERE code_alpha2 = 'US';

INSERT INTO states (name, code, country_id, timezone_primary, sort_order, is_active, created_at) 
SELECT 'Arizona', 'AZ', id, 'America/Phoenix', 3, TRUE, NOW() FROM countries WHERE code_alpha2 = 'US';

INSERT INTO states (name, code, country_id, timezone_primary, sort_order, is_active, created_at) 
SELECT 'Arkansas', 'AR', id, 'America/Chicago', 4, TRUE, NOW() FROM countries WHERE code_alpha2 = 'US';

INSERT INTO states (name, code, country_id, timezone_primary, sort_order, is_active, created_at) 
SELECT 'California', 'CA', id, 'America/Los_Angeles', 5, TRUE, NOW() FROM countries WHERE code_alpha2 = 'US';

INSERT INTO states (name, code, country_id, timezone_primary, sort_order, is_active, created_at) 
SELECT 'Colorado', 'CO', id, 'America/Denver', 6, TRUE, NOW() FROM countries WHERE code_alpha2 = 'US';

INSERT INTO states (name, code, country_id, timezone_primary, sort_order, is_active, created_at) 
SELECT 'Connecticut', 'CT', id, 'America/New_York', 7, TRUE, NOW() FROM countries WHERE code_alpha2 = 'US';

INSERT INTO states (name, code, country_id, timezone_primary, sort_order, is_active, created_at) 
SELECT 'Delaware', 'DE', id, 'America/New_York', 8, TRUE, NOW() FROM countries WHERE code_alpha2 = 'US';

INSERT INTO states (name, code, country_id, timezone_primary, sort_order, is_active, created_at) 
SELECT 'Florida', 'FL', id, 'America/New_York', 9, TRUE, NOW() FROM countries WHERE code_alpha2 = 'US';

INSERT INTO states (name, code, country_id, timezone_primary, sort_order, is_active, created_at) 
SELECT 'Georgia', 'GA', id, 'America/New_York', 10, TRUE, NOW() FROM countries WHERE code_alpha2 = 'US';

INSERT INTO states (name, code, country_id, timezone_primary, sort_order, is_active, created_at) 
SELECT 'Hawaii', 'HI', id, 'Pacific/Honolulu', 11, TRUE, NOW() FROM countries WHERE code_alpha2 = 'US';

INSERT INTO states (name, code, country_id, timezone_primary, sort_order, is_active, created_at) 
SELECT 'Idaho', 'ID', id, 'America/Boise', 12, TRUE, NOW() FROM countries WHERE code_alpha2 = 'US';

INSERT INTO states (name, code, country_id, timezone_primary, sort_order, is_active, created_at) 
SELECT 'Illinois', 'IL', id, 'America/Chicago', 13, TRUE, NOW() FROM countries WHERE code_alpha2 = 'US';

INSERT INTO states (name, code, country_id, timezone_primary, sort_order, is_active, created_at) 
SELECT 'Indiana', 'IN', id, 'America/New_York', 14, TRUE, NOW() FROM countries WHERE code_alpha2 = 'US';

INSERT INTO states (name, code, country_id, timezone_primary, sort_order, is_active, created_at) 
SELECT 'Iowa', 'IA', id, 'America/Chicago', 15, TRUE, NOW() FROM countries WHERE code_alpha2 = 'US';

INSERT INTO states (name, code, country_id, timezone_primary, sort_order, is_active, created_at) 
SELECT 'Kansas', 'KS', id, 'America/Chicago', 16, TRUE, NOW() FROM countries WHERE code_alpha2 = 'US';

INSERT INTO states (name, code, country_id, timezone_primary, sort_order, is_active, created_at) 
SELECT 'Kentucky', 'KY', id, 'America/New_York', 17, TRUE, NOW() FROM countries WHERE code_alpha2 = 'US';

INSERT INTO states (name, code, country_id, timezone_primary, sort_order, is_active, created_at) 
SELECT 'Louisiana', 'LA', id, 'America/Chicago', 18, TRUE, NOW() FROM countries WHERE code_alpha2 = 'US';

INSERT INTO states (name, code, country_id, timezone_primary, sort_order, is_active, created_at) 
SELECT 'Maine', 'ME', id, 'America/New_York', 19, TRUE, NOW() FROM countries WHERE code_alpha2 = 'US';

INSERT INTO states (name, code, country_id, timezone_primary, sort_order, is_active, created_at) 
SELECT 'Maryland', 'MD', id, 'America/New_York', 20, TRUE, NOW() FROM countries WHERE code_alpha2 = 'US';

INSERT INTO states (name, code, country_id, timezone_primary, sort_order, is_active, created_at) 
SELECT 'Massachusetts', 'MA', id, 'America/New_York', 21, TRUE, NOW() FROM countries WHERE code_alpha2 = 'US';

INSERT INTO states (name, code, country_id, timezone_primary, sort_order, is_active, created_at) 
SELECT 'Michigan', 'MI', id, 'America/New_York', 22, TRUE, NOW() FROM countries WHERE code_alpha2 = 'US';

INSERT INTO states (name, code, country_id, timezone_primary, sort_order, is_active, created_at) 
SELECT 'Minnesota', 'MN', id, 'America/Chicago', 23, TRUE, NOW() FROM countries WHERE code_alpha2 = 'US';

INSERT INTO states (name, code, country_id, timezone_primary, sort_order, is_active, created_at) 
SELECT 'Mississippi', 'MS', id, 'America/Chicago', 24, TRUE, NOW() FROM countries WHERE code_alpha2 = 'US';

INSERT INTO states (name, code, country_id, timezone_primary, sort_order, is_active, created_at) 
SELECT 'Missouri', 'MO', id, 'America/Chicago', 25, TRUE, NOW() FROM countries WHERE code_alpha2 = 'US';

INSERT INTO states (name, code, country_id, timezone_primary, sort_order, is_active, created_at) 
SELECT 'Montana', 'MT', id, 'America/Denver', 26, TRUE, NOW() FROM countries WHERE code_alpha2 = 'US';

INSERT INTO states (name, code, country_id, timezone_primary, sort_order, is_active, created_at) 
SELECT 'Nebraska', 'NE', id, 'America/Chicago', 27, TRUE, NOW() FROM countries WHERE code_alpha2 = 'US';

INSERT INTO states (name, code, country_id, timezone_primary, sort_order, is_active, created_at) 
SELECT 'Nevada', 'NV', id, 'America/Los_Angeles', 28, TRUE, NOW() FROM countries WHERE code_alpha2 = 'US';

INSERT INTO states (name, code, country_id, timezone_primary, sort_order, is_active, created_at) 
SELECT 'New Hampshire', 'NH', id, 'America/New_York', 29, TRUE, NOW() FROM countries WHERE code_alpha2 = 'US';

INSERT INTO states (name, code, country_id, timezone_primary, sort_order, is_active, created_at) 
SELECT 'New Jersey', 'NJ', id, 'America/New_York', 30, TRUE, NOW() FROM countries WHERE code_alpha2 = 'US';

INSERT INTO states (name, code, country_id, timezone_primary, sort_order, is_active, created_at) 
SELECT 'New Mexico', 'NM', id, 'America/Denver', 31, TRUE, NOW() FROM countries WHERE code_alpha2 = 'US';

INSERT INTO states (name, code, country_id, timezone_primary, sort_order, is_active, created_at) 
SELECT 'New York', 'NY', id, 'America/New_York', 32, TRUE, NOW() FROM countries WHERE code_alpha2 = 'US';

INSERT INTO states (name, code, country_id, timezone_primary, sort_order, is_active, created_at) 
SELECT 'North Carolina', 'NC', id, 'America/New_York', 33, TRUE, NOW() FROM countries WHERE code_alpha2 = 'US';

INSERT INTO states (name, code, country_id, timezone_primary, sort_order, is_active, created_at) 
SELECT 'North Dakota', 'ND', id, 'America/Chicago', 34, TRUE, NOW() FROM countries WHERE code_alpha2 = 'US';

INSERT INTO states (name, code, country_id, timezone_primary, sort_order, is_active, created_at) 
SELECT 'Ohio', 'OH', id, 'America/New_York', 35, TRUE, NOW() FROM countries WHERE code_alpha2 = 'US';

INSERT INTO states (name, code, country_id, timezone_primary, sort_order, is_active, created_at) 
SELECT 'Oklahoma', 'OK', id, 'America/Chicago', 36, TRUE, NOW() FROM countries WHERE code_alpha2 = 'US';

INSERT INTO states (name, code, country_id, timezone_primary, sort_order, is_active, created_at) 
SELECT 'Oregon', 'OR', id, 'America/Los_Angeles', 37, TRUE, NOW() FROM countries WHERE code_alpha2 = 'US';

INSERT INTO states (name, code, country_id, timezone_primary, sort_order, is_active, created_at) 
SELECT 'Pennsylvania', 'PA', id, 'America/New_York', 38, TRUE, NOW() FROM countries WHERE code_alpha2 = 'US';

INSERT INTO states (name, code, country_id, timezone_primary, sort_order, is_active, created_at) 
SELECT 'Rhode Island', 'RI', id, 'America/New_York', 39, TRUE, NOW() FROM countries WHERE code_alpha2 = 'US';

INSERT INTO states (name, code, country_id, timezone_primary, sort_order, is_active, created_at) 
SELECT 'South Carolina', 'SC', id, 'America/New_York', 40, TRUE, NOW() FROM countries WHERE code_alpha2 = 'US';

INSERT INTO states (name, code, country_id, timezone_primary, sort_order, is_active, created_at) 
SELECT 'South Dakota', 'SD', id, 'America/Chicago', 41, TRUE, NOW() FROM countries WHERE code_alpha2 = 'US';

INSERT INTO states (name, code, country_id, timezone_primary, sort_order, is_active, created_at) 
SELECT 'Tennessee', 'TN', id, 'America/Chicago', 42, TRUE, NOW() FROM countries WHERE code_alpha2 = 'US';

INSERT INTO states (name, code, country_id, timezone_primary, sort_order, is_active, created_at) 
SELECT 'Texas', 'TX', id, 'America/Chicago', 43, TRUE, NOW() FROM countries WHERE code_alpha2 = 'US';

INSERT INTO states (name, code, country_id, timezone_primary, sort_order, is_active, created_at) 
SELECT 'Utah', 'UT', id, 'America/Denver', 44, TRUE, NOW() FROM countries WHERE code_alpha2 = 'US';

INSERT INTO states (name, code, country_id, timezone_primary, sort_order, is_active, created_at) 
SELECT 'Vermont', 'VT', id, 'America/New_York', 45, TRUE, NOW() FROM countries WHERE code_alpha2 = 'US';

INSERT INTO states (name, code, country_id, timezone_primary, sort_order, is_active, created_at) 
SELECT 'Virginia', 'VA', id, 'America/New_York', 46, TRUE, NOW() FROM countries WHERE code_alpha2 = 'US';

INSERT INTO states (name, code, country_id, timezone_primary, sort_order, is_active, created_at) 
SELECT 'Washington', 'WA', id, 'America/Los_Angeles', 47, TRUE, NOW() FROM countries WHERE code_alpha2 = 'US';

INSERT INTO states (name, code, country_id, timezone_primary, sort_order, is_active, created_at) 
SELECT 'West Virginia', 'WV', id, 'America/New_York', 48, TRUE, NOW() FROM countries WHERE code_alpha2 = 'US';

INSERT INTO states (name, code, country_id, timezone_primary, sort_order, is_active, created_at) 
SELECT 'Wisconsin', 'WI', id, 'America/Chicago', 49, TRUE, NOW() FROM countries WHERE code_alpha2 = 'US';

INSERT INTO states (name, code, country_id, timezone_primary, sort_order, is_active, created_at) 
SELECT 'Wyoming', 'WY', id, 'America/Denver', 50, TRUE, NOW() FROM countries WHERE code_alpha2 = 'US';

-- Washington D.C.
INSERT INTO states (name, code, country_id, timezone_primary, sort_order, is_active, created_at) 
SELECT 'District of Columbia', 'DC', id, 'America/New_York', 51, TRUE, NOW() FROM countries WHERE code_alpha2 = 'US';

-- =====================================================
-- 3. PROVINCES - CANADA
-- =====================================================

INSERT INTO states (name, code, country_id, timezone_primary, sort_order, is_active, created_at) 
SELECT 'Alberta', 'AB', id, 'America/Edmonton', 1, TRUE, NOW() FROM countries WHERE code_alpha2 = 'CA';

INSERT INTO states (name, code, country_id, timezone_primary, sort_order, is_active, created_at) 
SELECT 'British Columbia', 'BC', id, 'America/Vancouver', 2, TRUE, NOW() FROM countries WHERE code_alpha2 = 'CA';

INSERT INTO states (name, code, country_id, timezone_primary, sort_order, is_active, created_at) 
SELECT 'Manitoba', 'MB', id, 'America/Winnipeg', 3, TRUE, NOW() FROM countries WHERE code_alpha2 = 'CA';

INSERT INTO states (name, code, country_id, timezone_primary, sort_order, is_active, created_at) 
SELECT 'New Brunswick', 'NB', id, 'America/Moncton', 4, TRUE, NOW() FROM countries WHERE code_alpha2 = 'CA';

INSERT INTO states (name, code, country_id, timezone_primary, sort_order, is_active, created_at) 
SELECT 'Newfoundland and Labrador', 'NL', id, 'America/St_Johns', 5, TRUE, NOW() FROM countries WHERE code_alpha2 = 'CA';

INSERT INTO states (name, code, country_id, timezone_primary, sort_order, is_active, created_at) 
SELECT 'Northwest Territories', 'NT', id, 'America/Yellowknife', 6, TRUE, NOW() FROM countries WHERE code_alpha2 = 'CA';

INSERT INTO states (name, code, country_id, timezone_primary, sort_order, is_active, created_at) 
SELECT 'Nova Scotia', 'NS', id, 'America/Halifax', 7, TRUE, NOW() FROM countries WHERE code_alpha2 = 'CA';

INSERT INTO states (name, code, country_id, timezone_primary, sort_order, is_active, created_at) 
SELECT 'Nunavut', 'NU', id, 'America/Iqaluit', 8, TRUE, NOW() FROM countries WHERE code_alpha2 = 'CA';

INSERT INTO states (name, code, country_id, timezone_primary, sort_order, is_active, created_at) 
SELECT 'Ontario', 'ON', id, 'America/Toronto', 9, TRUE, NOW() FROM countries WHERE code_alpha2 = 'CA';

INSERT INTO states (name, code, country_id, timezone_primary, sort_order, is_active, created_at) 
SELECT 'Prince Edward Island', 'PE', id, 'America/Halifax', 10, TRUE, NOW() FROM countries WHERE code_alpha2 = 'CA';

INSERT INTO states (name, code, country_id, timezone_primary, sort_order, is_active, created_at) 
SELECT 'Quebec', 'QC', id, 'America/Montreal', 11, TRUE, NOW() FROM countries WHERE code_alpha2 = 'CA';

INSERT INTO states (name, code, country_id, timezone_primary, sort_order, is_active, created_at) 
SELECT 'Saskatchewan', 'SK', id, 'America/Regina', 12, TRUE, NOW() FROM countries WHERE code_alpha2 = 'CA';

INSERT INTO states (name, code, country_id, timezone_primary, sort_order, is_active, created_at) 
SELECT 'Yukon', 'YT', id, 'America/Whitehorse', 13, TRUE, NOW() FROM countries WHERE code_alpha2 = 'CA';

-- =====================================================
-- 4. MAJOR CITIES - UNITED STATES
-- =====================================================

-- California Cities
INSERT INTO cities (name, state_id, latitude, longitude, population, timezone, postal_code, code, sort_order, is_active, created_at) 
SELECT 'Los Angeles', id, 34.0522, -118.2437, 3971883, 'America/Los_Angeles', '90210', 'LA', 1, TRUE, NOW() 
FROM states WHERE name = 'California' AND country_id = (SELECT id FROM countries WHERE code_alpha2 = 'US');

INSERT INTO cities (name, state_id, latitude, longitude, population, timezone, postal_code, code, sort_order, is_active, created_at) 
SELECT 'San Francisco', id, 37.7749, -122.4194, 881549, 'America/Los_Angeles', '94102', 'SF', 2, TRUE, NOW() 
FROM states WHERE name = 'California' AND country_id = (SELECT id FROM countries WHERE code_alpha2 = 'US');

INSERT INTO cities (name, state_id, latitude, longitude, population, timezone, postal_code, code, sort_order, is_active, created_at) 
SELECT 'San Diego', id, 32.7157, -117.1611, 1423851, 'America/Los_Angeles', '92101', 'SD', 3, TRUE, NOW() 
FROM states WHERE name = 'California' AND country_id = (SELECT id FROM countries WHERE code_alpha2 = 'US');

INSERT INTO cities (name, state_id, latitude, longitude, population, timezone, postal_code, code, sort_order, is_active, created_at) 
SELECT 'San Jose', id, 37.3382, -121.8863, 1013240, 'America/Los_Angeles', '95113', 'SJ', 4, TRUE, NOW() 
FROM states WHERE name = 'California' AND country_id = (SELECT id FROM countries WHERE code_alpha2 = 'US');

INSERT INTO cities (name, state_id, latitude, longitude, population, timezone, postal_code, code, sort_order, is_active, created_at) 
SELECT 'Sacramento', id, 38.5816, -121.4944, 508529, 'America/Los_Angeles', '95814', 'SAC', 5, TRUE, NOW() 
FROM states WHERE name = 'California' AND country_id = (SELECT id FROM countries WHERE code_alpha2 = 'US');

-- New York Cities
INSERT INTO cities (name, state_id, latitude, longitude, population, timezone, postal_code, code, sort_order, is_active, created_at) 
SELECT 'New York City', id, 40.7128, -74.0060, 8336817, 'America/New_York', '10001', 'NYC', 1, TRUE, NOW() 
FROM states WHERE name = 'New York' AND country_id = (SELECT id FROM countries WHERE code_alpha2 = 'US');

INSERT INTO cities (name, state_id, latitude, longitude, population, timezone, postal_code, code, sort_order, is_active, created_at) 
SELECT 'Buffalo', id, 42.8864, -78.8784, 255284, 'America/New_York', '14201', 'BUF', 2, TRUE, NOW() 
FROM states WHERE name = 'New York' AND country_id = (SELECT id FROM countries WHERE code_alpha2 = 'US');

INSERT INTO cities (name, state_id, latitude, longitude, population, timezone, postal_code, code, sort_order, is_active, created_at) 
SELECT 'Rochester', id, 43.1566, -77.6088, 205695, 'America/New_York', '14604', 'ROC', 3, TRUE, NOW() 
FROM states WHERE name = 'New York' AND country_id = (SELECT id FROM countries WHERE code_alpha2 = 'US');

INSERT INTO cities (name, state_id, latitude, longitude, population, timezone, postal_code, code, sort_order, is_active, created_at) 
SELECT 'Albany', id, 42.6526, -73.7562, 96460, 'America/New_York', '12207', 'ALB', 4, TRUE, NOW() 
FROM states WHERE name = 'New York' AND country_id = (SELECT id FROM countries WHERE code_alpha2 = 'US');

-- Texas Cities
INSERT INTO cities (name, state_id, latitude, longitude, population, timezone, postal_code, code, sort_order, is_active, created_at) 
SELECT 'Houston', id, 29.7604, -95.3698, 2320268, 'America/Chicago', '77002', 'HOU', 1, TRUE, NOW() 
FROM states WHERE name = 'Texas' AND country_id = (SELECT id FROM countries WHERE code_alpha2 = 'US');

INSERT INTO cities (name, state_id, latitude, longitude, population, timezone, postal_code, code, sort_order, is_active, created_at) 
SELECT 'Austin', id, 30.2672, -97.7431, 978908, 'America/Chicago', '78701', 'AUS', 2, TRUE, NOW() 
FROM states WHERE name = 'Texas' AND country_id = (SELECT id FROM countries WHERE code_alpha2 = 'US');

INSERT INTO cities (name, state_id, latitude, longitude, population, timezone, postal_code, code, sort_order, is_active, created_at) 
SELECT 'Dallas', id, 32.7767, -96.7970, 1343573, 'America/Chicago', '75201', 'DAL', 3, TRUE, NOW() 
FROM states WHERE name = 'Texas' AND country_id = (SELECT id FROM countries WHERE code_alpha2 = 'US');

INSERT INTO cities (name, state_id, latitude, longitude, population, timezone, postal_code, code, sort_order, is_active, created_at) 
SELECT 'San Antonio', id, 29.4241, -98.4936, 1547253, 'America/Chicago', '78205', 'SA', 4, TRUE, NOW() 
FROM states WHERE name = 'Texas' AND country_id = (SELECT id FROM countries WHERE code_alpha2 = 'US');

-- Florida Cities
INSERT INTO cities (name, state_id, latitude, longitude, population, timezone, postal_code, code, sort_order, is_active, created_at) 
SELECT 'Miami', id, 25.7617, -80.1918, 467963, 'America/New_York', '33101', 'MIA', 1, TRUE, NOW() 
FROM states WHERE name = 'Florida' AND country_id = (SELECT id FROM countries WHERE code_alpha2 = 'US');

INSERT INTO cities (name, state_id, latitude, longitude, population, timezone, postal_code, code, sort_order, is_active, created_at) 
SELECT 'Orlando', id, 28.5383, -81.3792, 307573, 'America/New_York', '32801', 'ORL', 2, TRUE, NOW() 
FROM states WHERE name = 'Florida' AND country_id = (SELECT id FROM countries WHERE code_alpha2 = 'US');

INSERT INTO cities (name, state_id, latitude, longitude, population, timezone, postal_code, code, sort_order, is_active, created_at) 
SELECT 'Tampa', id, 27.9506, -82.4572, 399700, 'America/New_York', '33602', 'TPA', 3, TRUE, NOW() 
FROM states WHERE name = 'Florida' AND country_id = (SELECT id FROM countries WHERE code_alpha2 = 'US');

INSERT INTO cities (name, state_id, latitude, longitude, population, timezone, postal_code, code, sort_order, is_active, created_at) 
SELECT 'Jacksonville', id, 30.3322, -81.6557, 949611, 'America/New_York', '32099', 'JAX', 4, TRUE, NOW() 
FROM states WHERE name = 'Florida' AND country_id = (SELECT id FROM countries WHERE code_alpha2 = 'US');

-- Washington Cities
INSERT INTO cities (name, state_id, latitude, longitude, population, timezone, postal_code, code, sort_order, is_active, created_at) 
SELECT 'Seattle', id, 47.6062, -122.3321, 753675, 'America/Los_Angeles', '98101', 'SEA', 1, TRUE, NOW() 
FROM states WHERE name = 'Washington' AND country_id = (SELECT id FROM countries WHERE code_alpha2 = 'US');

INSERT INTO cities (name, state_id, latitude, longitude, population, timezone, postal_code, code, sort_order, is_active, created_at) 
SELECT 'Spokane', id, 47.6588, -117.4260, 230176, 'America/Los_Angeles', '99201', 'GEG', 2, TRUE, NOW() 
FROM states WHERE name = 'Washington' AND country_id = (SELECT id FROM countries WHERE code_alpha2 = 'US');

INSERT INTO cities (name, state_id, latitude, longitude, population, timezone, postal_code, code, sort_order, is_active, created_at) 
SELECT 'Tacoma', id, 47.2529, -122.4443, 219346, 'America/Los_Angeles', '98402', 'TAC', 3, TRUE, NOW() 
FROM states WHERE name = 'Washington' AND country_id = (SELECT id FROM countries WHERE code_alpha2 = 'US');

-- Illinois Cities
INSERT INTO cities (name, state_id, latitude, longitude, population, timezone, postal_code, code, sort_order, is_active, created_at) 
SELECT 'Chicago', id, 41.8781, -87.6298, 2695598, 'America/Chicago', '60601', 'CHI', 1, TRUE, NOW() 
FROM states WHERE name = 'Illinois' AND country_id = (SELECT id FROM countries WHERE code_alpha2 = 'US');

-- Massachusetts Cities
INSERT INTO cities (name, state_id, latitude, longitude, population, timezone, postal_code, code, sort_order, is_active, created_at) 
SELECT 'Boston', id, 42.3601, -71.0589, 695506, 'America/New_York', '02101', 'BOS', 1, TRUE, NOW() 
FROM states WHERE name = 'Massachusetts' AND country_id = (SELECT id FROM countries WHERE code_alpha2 = 'US');

-- Pennsylvania Cities
INSERT INTO cities (name, state_id, latitude, longitude, population, timezone, postal_code, code, sort_order, is_active, created_at) 
SELECT 'Philadelphia', id, 39.9526, -75.1652, 1584064, 'America/New_York', '19101', 'PHL', 1, TRUE, NOW() 
FROM states WHERE name = 'Pennsylvania' AND country_id = (SELECT id FROM countries WHERE code_alpha2 = 'US');

-- Georgia Cities
INSERT INTO cities (name, state_id, latitude, longitude, population, timezone, postal_code, code, sort_order, is_active, created_at) 
SELECT 'Atlanta', id, 33.7490, -84.3880, 498715, 'America/New_York', '30301', 'ATL', 1, TRUE, NOW() 
FROM states WHERE name = 'Georgia' AND country_id = (SELECT id FROM countries WHERE code_alpha2 = 'US');

-- Colorado Cities
INSERT INTO cities (name, state_id, latitude, longitude, population, timezone, postal_code, code, sort_order, is_active, created_at) 
SELECT 'Denver', id, 39.7392, -104.9903, 715522, 'America/Denver', '80202', 'DEN', 1, TRUE, NOW() 
FROM states WHERE name = 'Colorado' AND country_id = (SELECT id FROM countries WHERE code_alpha2 = 'US');

-- District of Columbia
INSERT INTO cities (name, state_id, latitude, longitude, population, timezone, postal_code, code, sort_order, is_active, created_at) 
SELECT 'Washington', id, 38.9072, -77.0369, 689545, 'America/New_York', '20001', 'DC', 1, TRUE, NOW() 
FROM states WHERE name = 'District of Columbia' AND country_id = (SELECT id FROM countries WHERE code_alpha2 = 'US');

-- =====================================================
-- 5. MAJOR CITIES - CANADA
-- =====================================================

-- Ontario Cities
INSERT INTO cities (name, state_id, latitude, longitude, population, timezone, postal_code, code, sort_order, is_active, created_at) 
SELECT 'Toronto', id, 43.6532, -79.3832, 2794356, 'America/Toronto', 'M5H', 'TOR', 1, TRUE, NOW() 
FROM states WHERE name = 'Ontario' AND country_id = (SELECT id FROM countries WHERE code_alpha2 = 'CA');

INSERT INTO cities (name, state_id, latitude, longitude, population, timezone, postal_code, code, sort_order, is_active, created_at) 
SELECT 'Ottawa', id, 45.4215, -75.6972, 1017449, 'America/Toronto', 'K1A', 'OTT', 2, TRUE, NOW() 
FROM states WHERE name = 'Ontario' AND country_id = (SELECT id FROM countries WHERE code_alpha2 = 'CA');

INSERT INTO cities (name, state_id, latitude, longitude, population, timezone, postal_code, code, sort_order, is_active, created_at) 
SELECT 'Hamilton', id, 43.2557, -79.8711, 569353, 'America/Toronto', 'L8P', 'HAM', 3, TRUE, NOW() 
FROM states WHERE name = 'Ontario' AND country_id = (SELECT id FROM countries WHERE code_alpha2 = 'CA');

INSERT INTO cities (name, state_id, latitude, longitude, population, timezone, postal_code, code, sort_order, is_active, created_at) 
SELECT 'London', id, 42.9849, -81.2453, 422324, 'America/Toronto', 'N6A', 'LDN', 4, TRUE, NOW() 
FROM states WHERE name = 'Ontario' AND country_id = (SELECT id FROM countries WHERE code_alpha2 = 'CA');

-- Quebec Cities
INSERT INTO cities (name, state_id, latitude, longitude, population, timezone, postal_code, code, sort_order, is_active, created_at) 
SELECT 'Montreal', id, 45.5017, -73.5673, 1780000, 'America/Montreal', 'H2Y', 'MTL', 1, TRUE, NOW() 
FROM states WHERE name = 'Quebec' AND country_id = (SELECT id FROM countries WHERE code_alpha2 = 'CA');

INSERT INTO cities (name, state_id, latitude, longitude, population, timezone, postal_code, code, sort_order, is_active, created_at) 
SELECT 'Quebec City', id, 46.8139, -71.2080, 542298, 'America/Montreal', 'G1R', 'QC', 2, TRUE, NOW() 
FROM states WHERE name = 'Quebec' AND country_id = (SELECT id FROM countries WHERE code_alpha2 = 'CA');

-- British Columbia Cities
INSERT INTO cities (name, state_id, latitude, longitude, population, timezone, postal_code, code, sort_order, is_active, created_at) 
SELECT 'Vancouver', id, 49.2827, -123.1207, 675218, 'America/Vancouver', 'V6B', 'VAN', 1, TRUE, NOW() 
FROM states WHERE name = 'British Columbia' AND country_id = (SELECT id FROM countries WHERE code_alpha2 = 'CA');

INSERT INTO cities (name, state_id, latitude, longitude, population, timezone, postal_code, code, sort_order, is_active, created_at) 
SELECT 'Victoria', id, 48.4284, -123.3656, 91867, 'America/Vancouver', 'V8W', 'VIC', 2, TRUE, NOW() 
FROM states WHERE name = 'British Columbia' AND country_id = (SELECT id FROM countries WHERE code_alpha2 = 'CA');

INSERT INTO cities (name, state_id, latitude, longitude, population, timezone, postal_code, code, sort_order, is_active, created_at) 
SELECT 'Burnaby', id, 49.2488, -122.9805, 249125, 'America/Vancouver', 'V5H', 'BUR', 3, TRUE, NOW() 
FROM states WHERE name = 'British Columbia' AND country_id = (SELECT id FROM countries WHERE code_alpha2 = 'CA');

-- Alberta Cities
INSERT INTO cities (name, state_id, latitude, longitude, population, timezone, postal_code, code, sort_order, is_active, created_at) 
SELECT 'Calgary', id, 51.0447, -114.0719, 1306784, 'America/Edmonton', 'T2P', 'CAL', 1, TRUE, NOW() 
FROM states WHERE name = 'Alberta' AND country_id = (SELECT id FROM countries WHERE code_alpha2 = 'CA');

INSERT INTO cities (name, state_id, latitude, longitude, population, timezone, postal_code, code, sort_order, is_active, created_at) 
SELECT 'Edmonton', id, 53.5461, -113.4938, 981280, 'America/Edmonton', 'T5J', 'EDM', 2, TRUE, NOW() 
FROM states WHERE name = 'Alberta' AND country_id = (SELECT id FROM countries WHERE code_alpha2 = 'CA');

-- Manitoba Cities
INSERT INTO cities (name, state_id, latitude, longitude, population, timezone, postal_code, code, sort_order, is_active, created_at) 
SELECT 'Winnipeg', id, 49.8951, -97.1384, 749534, 'America/Winnipeg', 'R3C', 'WIN', 1, TRUE, NOW() 
FROM states WHERE name = 'Manitoba' AND country_id = (SELECT id FROM countries WHERE code_alpha2 = 'CA');

-- Nova Scotia Cities
INSERT INTO cities (name, state_id, latitude, longitude, population, timezone, postal_code, code, sort_order, is_active, created_at) 
SELECT 'Halifax', id, 44.6488, -63.5752, 439819, 'America/Halifax', 'B3J', 'HAL', 1, TRUE, NOW() 
FROM states WHERE name = 'Nova Scotia' AND country_id = (SELECT id FROM countries WHERE code_alpha2 = 'CA');

-- Saskatchewan Cities
INSERT INTO cities (name, state_id, latitude, longitude, population, timezone, postal_code, code, sort_order, is_active, created_at) 
SELECT 'Saskatoon', id, 52.1332, -106.6700, 317480, 'America/Regina', 'S7K', 'SAS', 1, TRUE, NOW() 
FROM states WHERE name = 'Saskatchewan' AND country_id = (SELECT id FROM countries WHERE code_alpha2 = 'CA');

INSERT INTO cities (name, state_id, latitude, longitude, population, timezone, postal_code, code, sort_order, is_active, created_at) 
SELECT 'Regina', id, 50.4452, -104.6189, 230139, 'America/Regina', 'S4P', 'REG', 2, TRUE, NOW() 
FROM states WHERE name = 'Saskatchewan' AND country_id = (SELECT id FROM countries WHERE code_alpha2 = 'CA');