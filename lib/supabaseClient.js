import { createClient } from "https://esm.sh/@supabase/supabase-js@2";

const supabaseUrl = "https://qeskvdvumufkvxfqfdkc.supabase.co";   // ✅ copy-paste from API Settings
const supabaseAnonKey = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InFlc2t2ZHV2bXVvZmt2eGZxZGtjIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjAwMzA5OTUsImV4cCI6MjA3NTYwNjk5NX0.Ah_ykA-s3-oTL150Ttb5YtZg0oMjiTzIEevCRPN70Xw";  // use the anon key from Settings → API Keys

export const supabase = createClient(supabaseUrl, supabaseAnonKey);
