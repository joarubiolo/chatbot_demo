CREATE TABLE IF NOT EXISTS reservations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    client_name TEXT NOT NULL,
    client_email TEXT NOT NULL,
    client_phone TEXT NOT NULL,
    service TEXT NOT NULL,
    date DATE NOT NULL,
    participants INTEGER NOT NULL DEFAULT 1,
    notes TEXT DEFAULT '',
    status TEXT NOT NULL DEFAULT 'pending' CHECK (status IN ('pending', 'confirmed', 'cancelled')),
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Índice para búsquedas por fecha
CREATE INDEX IF NOT EXISTS idx_reservations_date ON reservations(date);

-- Índice para filtrar por estado
CREATE INDEX IF NOT EXISTS idx_reservations_status ON reservations(status);

-- Política de seguridad: permitir lectura/escritura anónima (solo para este proyecto)
ALTER TABLE reservations ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Anyone can insert reservations"
    ON reservations FOR INSERT
    TO anon
    WITH CHECK (true);

CREATE POLICY "Anyone can view reservations"
    ON reservations FOR SELECT
    TO anon
    USING (true);
