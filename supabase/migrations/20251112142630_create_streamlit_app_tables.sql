/*
  # Streamlit App Database Schema

  1. New Tables
    - `users`
      - `id` (uuid, primary key)
      - `email` (text, unique)
      - `password_hash` (text) - bcrypt hashed password
      - `is_guest` (boolean) - flag for guest mode users
      - `created_at` (timestamptz)
    
    - `records`
      - `id` (uuid, primary key)
      - `user_id` (uuid, foreign key to users)
      - `title` (text)
      - `category` (text)
      - `value` (numeric)
      - `timestamp` (timestamptz)
      - `metadata` (jsonb) - flexible metadata storage
      - `created_at` (timestamptz)
      - `updated_at` (timestamptz)
    
    - `background_data`
      - `id` (uuid, primary key)
      - `source_url` (text)
      - `data` (jsonb)
      - `fetched_at` (timestamptz)
      - `status` (text) - success/error
      - `error_message` (text, nullable)

  2. Security
    - Enable RLS on all tables
    - Users can only access their own records
    - Background data is read-only for all authenticated users
*/

-- Create users table
CREATE TABLE IF NOT EXISTS users (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  email text UNIQUE NOT NULL,
  password_hash text NOT NULL,
  is_guest boolean DEFAULT false,
  created_at timestamptz DEFAULT now()
);

ALTER TABLE users ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can view own profile"
  ON users FOR SELECT
  TO authenticated
  USING (auth.uid() = id);

CREATE POLICY "Users can update own profile"
  ON users FOR UPDATE
  TO authenticated
  USING (auth.uid() = id)
  WITH CHECK (auth.uid() = id);

-- Create records table
CREATE TABLE IF NOT EXISTS records (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id uuid NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  title text NOT NULL,
  category text NOT NULL,
  value numeric NOT NULL DEFAULT 0,
  timestamp timestamptz NOT NULL DEFAULT now(),
  metadata jsonb DEFAULT '{}'::jsonb,
  created_at timestamptz DEFAULT now(),
  updated_at timestamptz DEFAULT now()
);

ALTER TABLE records ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can view own records"
  ON records FOR SELECT
  TO authenticated
  USING (user_id = auth.uid());

CREATE POLICY "Users can insert own records"
  ON records FOR INSERT
  TO authenticated
  WITH CHECK (user_id = auth.uid());

CREATE POLICY "Users can update own records"
  ON records FOR UPDATE
  TO authenticated
  USING (user_id = auth.uid())
  WITH CHECK (user_id = auth.uid());

CREATE POLICY "Users can delete own records"
  ON records FOR DELETE
  TO authenticated
  USING (user_id = auth.uid());

-- Create background_data table
CREATE TABLE IF NOT EXISTS background_data (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  source_url text NOT NULL,
  data jsonb DEFAULT '{}'::jsonb,
  fetched_at timestamptz DEFAULT now(),
  status text NOT NULL DEFAULT 'pending',
  error_message text
);

ALTER TABLE background_data ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Authenticated users can view background data"
  ON background_data FOR SELECT
  TO authenticated
  USING (true);

-- Create indexes for better query performance
CREATE INDEX IF NOT EXISTS idx_records_user_id ON records(user_id);
CREATE INDEX IF NOT EXISTS idx_records_category ON records(category);
CREATE INDEX IF NOT EXISTS idx_records_timestamp ON records(timestamp);
CREATE INDEX IF NOT EXISTS idx_background_data_fetched_at ON background_data(fetched_at DESC);