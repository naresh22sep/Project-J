-- =====================================================
-- LOCATION MANAGEMENT - USA & CANADA FOCUS (CORRECTED)
-- =====================================================

USE jobhunter_fresh;

-- =====================================================
-- TRUNCATE TABLES BEFORE INSERTING NEW DATA
-- =====================================================

-- Disable foreign key checks temporarily
SET FOREIGN_KEY_CHECKS = 0;

-- Truncate tables in dependency order (cities -> states -> countries)
TRUNCATE TABLE cities;
TRUNCATE TABLE states;
TRUNCATE TABLE countries;

-- Reset AUTO_INCREMENT counters
ALTER TABLE countries AUTO_INCREMENT = 1;
ALTER TABLE states AUTO_INCREMENT = 1;
ALTER TABLE cities AUTO_INCREMENT = 1;

-- Re-enable foreign key checks
SET FOREIGN_KEY_CHECKS = 1;

-- =====================================================
-- 1. COUNTRIES (USA & CANADA) - Including all required codes
-- =====================================================

INSERT INTO countries (name, code_alpha2, code_alpha3, is_active) VALUES
('United States', 'US', 'USA', 1),
('Canada', 'CA', 'CAN', 1);

-- =====================================================
-- 2. STATES/PROVINCES - Including required code
-- =====================================================

-- Get country IDs for reference
SET @usa_id = (SELECT id FROM countries WHERE code_alpha2 = 'US');
SET @canada_id = (SELECT id FROM countries WHERE code_alpha2 = 'CA');

-- US States (including state codes)
INSERT INTO states (name, code, country_id, is_active) VALUES
('Alabama', 'AL', @usa_id, 1),
('Alaska', 'AK', @usa_id, 1),
('Arizona', 'AZ', @usa_id, 1),
('Arkansas', 'AR', @usa_id, 1),
('California', 'CA', @usa_id, 1),
('Colorado', 'CO', @usa_id, 1),
('Connecticut', 'CT', @usa_id, 1),
('Delaware', 'DE', @usa_id, 1),
('Florida', 'FL', @usa_id, 1),
('Georgia', 'GA', @usa_id, 1),
('Hawaii', 'HI', @usa_id, 1),
('Idaho', 'ID', @usa_id, 1),
('Illinois', 'IL', @usa_id, 1),
('Indiana', 'IN', @usa_id, 1),
('Iowa', 'IA', @usa_id, 1),
('Kansas', 'KS', @usa_id, 1),
('Kentucky', 'KY', @usa_id, 1),
('Louisiana', 'LA', @usa_id, 1),
('Maine', 'ME', @usa_id, 1),
('Maryland', 'MD', @usa_id, 1),
('Massachusetts', 'MA', @usa_id, 1),
('Michigan', 'MI', @usa_id, 1),
('Minnesota', 'MN', @usa_id, 1),
('Mississippi', 'MS', @usa_id, 1),
('Missouri', 'MO', @usa_id, 1),
('Montana', 'MT', @usa_id, 1),
('Nebraska', 'NE', @usa_id, 1),
('Nevada', 'NV', @usa_id, 1),
('New Hampshire', 'NH', @usa_id, 1),
('New Jersey', 'NJ', @usa_id, 1),
('New Mexico', 'NM', @usa_id, 1),
('New York', 'NY', @usa_id, 1),
('North Carolina', 'NC', @usa_id, 1),
('North Dakota', 'ND', @usa_id, 1),
('Ohio', 'OH', @usa_id, 1),
('Oklahoma', 'OK', @usa_id, 1),
('Oregon', 'OR', @usa_id, 1),
('Pennsylvania', 'PA', @usa_id, 1),
('Rhode Island', 'RI', @usa_id, 1),
('South Carolina', 'SC', @usa_id, 1),
('South Dakota', 'SD', @usa_id, 1),
('Tennessee', 'TN', @usa_id, 1),
('Texas', 'TX', @usa_id, 1),
('Utah', 'UT', @usa_id, 1),
('Vermont', 'VT', @usa_id, 1),
('Virginia', 'VA', @usa_id, 1),
('Washington', 'WA', @usa_id, 1),
('West Virginia', 'WV', @usa_id, 1),
('Wisconsin', 'WI', @usa_id, 1),
('Wyoming', 'WY', @usa_id, 1),
('District of Columbia', 'DC', @usa_id, 1);

-- Canadian Provinces (including province codes)
INSERT INTO states (name, code, country_id, is_active) VALUES
('Alberta', 'AB', @canada_id, 1),
('British Columbia', 'BC', @canada_id, 1),
('Manitoba', 'MB', @canada_id, 1),
('New Brunswick', 'NB', @canada_id, 1),
('Newfoundland and Labrador', 'NL', @canada_id, 1),
('Northwest Territories', 'NT', @canada_id, 1),
('Nova Scotia', 'NS', @canada_id, 1),
('Nunavut', 'NU', @canada_id, 1),
('Ontario', 'ON', @canada_id, 1),
('Prince Edward Island', 'PE', @canada_id, 1),
('Quebec', 'QC', @canada_id, 1),
('Saskatchewan', 'SK', @canada_id, 1),
('Yukon', 'YT', @canada_id, 1);

-- =====================================================
-- 3. MAJOR CITIES - Tech Hubs Focus
-- =====================================================

-- Major US Cities (Tech Hubs)
INSERT INTO cities (name, state_id, is_active) VALUES
-- California Tech Cities (Silicon Valley & Beyond)
('San Francisco', (SELECT id FROM states WHERE code = 'CA' AND country_id = @usa_id), 1),
('San Jose', (SELECT id FROM states WHERE code = 'CA' AND country_id = @usa_id), 1),
('Los Angeles', (SELECT id FROM states WHERE code = 'CA' AND country_id = @usa_id), 1),
('San Diego', (SELECT id FROM states WHERE code = 'CA' AND country_id = @usa_id), 1),
('Sacramento', (SELECT id FROM states WHERE code = 'CA' AND country_id = @usa_id), 1),
('Oakland', (SELECT id FROM states WHERE code = 'CA' AND country_id = @usa_id), 1),
('Santa Clara', (SELECT id FROM states WHERE code = 'CA' AND country_id = @usa_id), 1),
('Palo Alto', (SELECT id FROM states WHERE code = 'CA' AND country_id = @usa_id), 1),
('Mountain View', (SELECT id FROM states WHERE code = 'CA' AND country_id = @usa_id), 1),
('Sunnyvale', (SELECT id FROM states WHERE code = 'CA' AND country_id = @usa_id), 1),
('Cupertino', (SELECT id FROM states WHERE code = 'CA' AND country_id = @usa_id), 1),
('Redwood City', (SELECT id FROM states WHERE code = 'CA' AND country_id = @usa_id), 1),

-- New York Tech Cities
('New York City', (SELECT id FROM states WHERE code = 'NY' AND country_id = @usa_id), 1),
('Buffalo', (SELECT id FROM states WHERE code = 'NY' AND country_id = @usa_id), 1),
('Rochester', (SELECT id FROM states WHERE code = 'NY' AND country_id = @usa_id), 1),
('Albany', (SELECT id FROM states WHERE code = 'NY' AND country_id = @usa_id), 1),
('Syracuse', (SELECT id FROM states WHERE code = 'NY' AND country_id = @usa_id), 1),

-- Texas Tech Cities
('Austin', (SELECT id FROM states WHERE code = 'TX' AND country_id = @usa_id), 1),
('Houston', (SELECT id FROM states WHERE code = 'TX' AND country_id = @usa_id), 1),
('Dallas', (SELECT id FROM states WHERE code = 'TX' AND country_id = @usa_id), 1),
('San Antonio', (SELECT id FROM states WHERE code = 'TX' AND country_id = @usa_id), 1),
('Fort Worth', (SELECT id FROM states WHERE code = 'TX' AND country_id = @usa_id), 1),
('Plano', (SELECT id FROM states WHERE code = 'TX' AND country_id = @usa_id), 1),
('Irving', (SELECT id FROM states WHERE code = 'TX' AND country_id = @usa_id), 1),

-- Washington Tech Cities
('Seattle', (SELECT id FROM states WHERE code = 'WA' AND country_id = @usa_id), 1),
('Redmond', (SELECT id FROM states WHERE code = 'WA' AND country_id = @usa_id), 1),
('Bellevue', (SELECT id FROM states WHERE code = 'WA' AND country_id = @usa_id), 1),
('Tacoma', (SELECT id FROM states WHERE code = 'WA' AND country_id = @usa_id), 1),
('Spokane', (SELECT id FROM states WHERE code = 'WA' AND country_id = @usa_id), 1),

-- Other Major Tech Hubs
('Chicago', (SELECT id FROM states WHERE code = 'IL' AND country_id = @usa_id), 1),
('Boston', (SELECT id FROM states WHERE code = 'MA' AND country_id = @usa_id), 1),
('Cambridge', (SELECT id FROM states WHERE code = 'MA' AND country_id = @usa_id), 1),
('Philadelphia', (SELECT id FROM states WHERE code = 'PA' AND country_id = @usa_id), 1),
('Pittsburgh', (SELECT id FROM states WHERE code = 'PA' AND country_id = @usa_id), 1),
('Atlanta', (SELECT id FROM states WHERE code = 'GA' AND country_id = @usa_id), 1),
('Denver', (SELECT id FROM states WHERE code = 'CO' AND country_id = @usa_id), 1),
('Boulder', (SELECT id FROM states WHERE code = 'CO' AND country_id = @usa_id), 1),
('Phoenix', (SELECT id FROM states WHERE code = 'AZ' AND country_id = @usa_id), 1),
('Scottsdale', (SELECT id FROM states WHERE code = 'AZ' AND country_id = @usa_id), 1),
('Las Vegas', (SELECT id FROM states WHERE code = 'NV' AND country_id = @usa_id), 1),
('Portland', (SELECT id FROM states WHERE code = 'OR' AND country_id = @usa_id), 1),
('Nashville', (SELECT id FROM states WHERE code = 'TN' AND country_id = @usa_id), 1),
('Miami', (SELECT id FROM states WHERE code = 'FL' AND country_id = @usa_id), 1),
('Orlando', (SELECT id FROM states WHERE code = 'FL' AND country_id = @usa_id), 1),
('Tampa', (SELECT id FROM states WHERE code = 'FL' AND country_id = @usa_id), 1),
('Jacksonville', (SELECT id FROM states WHERE code = 'FL' AND country_id = @usa_id), 1),
('Washington DC', (SELECT id FROM states WHERE code = 'DC' AND country_id = @usa_id), 1),
('Detroit', (SELECT id FROM states WHERE code = 'MI' AND country_id = @usa_id), 1),
('Minneapolis', (SELECT id FROM states WHERE code = 'MN' AND country_id = @usa_id), 1),
('Charlotte', (SELECT id FROM states WHERE code = 'NC' AND country_id = @usa_id), 1),
('Raleigh', (SELECT id FROM states WHERE code = 'NC' AND country_id = @usa_id), 1),
('Durham', (SELECT id FROM states WHERE code = 'NC' AND country_id = @usa_id), 1),
('Baltimore', (SELECT id FROM states WHERE code = 'MD' AND country_id = @usa_id), 1),
('Columbus', (SELECT id FROM states WHERE code = 'OH' AND country_id = @usa_id), 1),
('Cleveland', (SELECT id FROM states WHERE code = 'OH' AND country_id = @usa_id), 1),
('Cincinnati', (SELECT id FROM states WHERE code = 'OH' AND country_id = @usa_id), 1),
('Indianapolis', (SELECT id FROM states WHERE code = 'IN' AND country_id = @usa_id), 1),
('Kansas City', (SELECT id FROM states WHERE code = 'MO' AND country_id = @usa_id), 1),
('St. Louis', (SELECT id FROM states WHERE code = 'MO' AND country_id = @usa_id), 1),
('Salt Lake City', (SELECT id FROM states WHERE code = 'UT' AND country_id = @usa_id), 1),
('Provo', (SELECT id FROM states WHERE code = 'UT' AND country_id = @usa_id), 1);

-- Major Canadian Cities (Tech Hubs)
INSERT INTO cities (name, state_id, is_active) VALUES
-- Ontario Tech Cities
('Toronto', (SELECT id FROM states WHERE code = 'ON' AND country_id = @canada_id), 1),
('Ottawa', (SELECT id FROM states WHERE code = 'ON' AND country_id = @canada_id), 1),
('Mississauga', (SELECT id FROM states WHERE code = 'ON' AND country_id = @canada_id), 1),
('Brampton', (SELECT id FROM states WHERE code = 'ON' AND country_id = @canada_id), 1),
('Hamilton', (SELECT id FROM states WHERE code = 'ON' AND country_id = @canada_id), 1),
('London', (SELECT id FROM states WHERE code = 'ON' AND country_id = @canada_id), 1),
('Markham', (SELECT id FROM states WHERE code = 'ON' AND country_id = @canada_id), 1),
('Vaughan', (SELECT id FROM states WHERE code = 'ON' AND country_id = @canada_id), 1),
('Kitchener', (SELECT id FROM states WHERE code = 'ON' AND country_id = @canada_id), 1),
('Waterloo', (SELECT id FROM states WHERE code = 'ON' AND country_id = @canada_id), 1),

-- Quebec Tech Cities
('Montreal', (SELECT id FROM states WHERE code = 'QC' AND country_id = @canada_id), 1),
('Quebec City', (SELECT id FROM states WHERE code = 'QC' AND country_id = @canada_id), 1),
('Laval', (SELECT id FROM states WHERE code = 'QC' AND country_id = @canada_id), 1),
('Gatineau', (SELECT id FROM states WHERE code = 'QC' AND country_id = @canada_id), 1),

-- British Columbia Tech Cities
('Vancouver', (SELECT id FROM states WHERE code = 'BC' AND country_id = @canada_id), 1),
('Victoria', (SELECT id FROM states WHERE code = 'BC' AND country_id = @canada_id), 1),
('Burnaby', (SELECT id FROM states WHERE code = 'BC' AND country_id = @canada_id), 1),
('Surrey', (SELECT id FROM states WHERE code = 'BC' AND country_id = @canada_id), 1),
('Richmond', (SELECT id FROM states WHERE code = 'BC' AND country_id = @canada_id), 1),

-- Alberta Tech Cities
('Calgary', (SELECT id FROM states WHERE code = 'AB' AND country_id = @canada_id), 1),
('Edmonton', (SELECT id FROM states WHERE code = 'AB' AND country_id = @canada_id), 1),

-- Other Canadian Tech Cities
('Winnipeg', (SELECT id FROM states WHERE code = 'MB' AND country_id = @canada_id), 1),
('Halifax', (SELECT id FROM states WHERE code = 'NS' AND country_id = @canada_id), 1),
('Saskatoon', (SELECT id FROM states WHERE code = 'SK' AND country_id = @canada_id), 1),
('Regina', (SELECT id FROM states WHERE code = 'SK' AND country_id = @canada_id), 1);

-- =====================================================
-- VERIFICATION
-- =====================================================

SELECT 'Location data import completed successfully!' as status;

SELECT 'Final Counts:' as info;
SELECT 'Countries' as table_name, COUNT(*) as record_count FROM countries WHERE is_active = 1
UNION ALL
SELECT 'States/Provinces', COUNT(*) FROM states WHERE is_active = 1
UNION ALL
SELECT 'Cities', COUNT(*) FROM cities WHERE is_active = 1;

-- Show sample data
SELECT 'Tech Hub Summary by Country:' as info;
SELECT 
    c.name as country,
    c.code_alpha2 as code_2,
    c.code_alpha3 as code_3,
    COUNT(DISTINCT s.id) as states_provinces,
    COUNT(ci.id) as tech_cities
FROM countries c 
JOIN states s ON c.id = s.country_id 
JOIN cities ci ON s.id = ci.state_id 
WHERE c.code_alpha2 IN ('US', 'CA')
GROUP BY c.id, c.name, c.code_alpha2, c.code_alpha3
ORDER BY c.name;

-- Show top tech states/provinces by city count
SELECT 'Top Tech States/Provinces:' as info;
SELECT 
    c.code_alpha2 as country,
    s.name as state_province,
    s.code,
    COUNT(ci.id) as cities
FROM countries c 
JOIN states s ON c.id = s.country_id 
JOIN cities ci ON s.id = ci.state_id 
WHERE c.code_alpha2 IN ('US', 'CA')
GROUP BY c.code_alpha2, s.id, s.name, s.code
HAVING COUNT(ci.id) >= 3
ORDER BY COUNT(ci.id) DESC, c.code_alpha2, s.name;

-- Sample cities by major tech hubs
SELECT 'Major US Tech Cities:' as info;
SELECT s.name as state, s.code, ci.name as city 
FROM states s 
JOIN cities ci ON s.id = ci.state_id 
JOIN countries c ON s.country_id = c.id
WHERE c.code_alpha2 = 'US' AND s.code IN ('CA', 'NY', 'TX', 'WA', 'MA')
ORDER BY s.name, ci.name
LIMIT 15;

SELECT 'Major Canadian Tech Cities:' as info;
SELECT s.name as province, s.code, ci.name as city 
FROM states s 
JOIN cities ci ON s.id = ci.state_id 
JOIN countries c ON s.country_id = c.id
WHERE c.code_alpha2 = 'CA'
ORDER BY s.name, ci.name
LIMIT 10;

SELECT 'Location data setup complete!' as final_status;