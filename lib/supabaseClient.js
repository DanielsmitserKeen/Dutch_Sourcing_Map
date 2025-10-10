// Import the Supabase client library from a CDN
import { createClient } from "https://esm.sh/@supabase/supabase-js@2";

// Your Supabase project URL and anon public key
const supabaseUrl = "https://qeskvdvmuofkxfqfdkc.supabase.co";
const supabaseAnonKey = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InFlc2t2ZHV2bXVvZmt2eGZxZGtjIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjAwMzA5OTUsImV4cCI6MjA3NTYwNjk5NX0.Ah_ykA-s3-oTL150Ttb5YtZg0oMjiTzIEevCRPN70Xw";

// Create a single Supabase client
export const supabase = createClient(supabaseUrl, supabaseAnonKey);
