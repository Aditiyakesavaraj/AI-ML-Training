CREATE TABLE plans (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    provider TEXT,
    data_per_day TEXT,
    validity TEXT,
    price INTEGER,
    extra TEXT
);

INSERT INTO plans (provider, data_per_day, validity, price, extra) VALUES
('Airtel', '1.5GB/day', '28 days', 479, 'Unlimited calls, OTT'),
('Jio', '2GB/day', '28 days', 499, 'Hotstar, unlimited calls'),
('VI', '3GB/day', '56 days', 699, 'Weekend rollover, calls');
