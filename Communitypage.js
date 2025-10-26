import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { MessageCircle, Send, Star } from 'lucide-react';

export default function SafePathCommunity() {
  const [messages, setMessages] = useState([
    { user: 'Rakesh', text: 'Be careful near Bliss Highway after 8PM, low lighting there.', rating: 3 },
    { user: 'Reshma', text: 'Safe and well-Cleaned around Tirumala!', rating: 5 },
  ]);
  const [input, setInput] = useState('');

  const sendMessage = () => {
    if (input.trim() === '') return;
    setMessages([...messages, { user: 'You', text: input, rating: 5 }]);
    setInput('');
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-950 via-indigo-950 to-black text-white p-8">
      <motion.h1
        className="text-4xl font-bold text-center mb-6 bg-gradient-to-r from-cyan-400 to-purple-500 text-transparent bg-clip-text"
        initial={{ opacity: 0, y: -40 }}
        animate={{ opacity: 1, y: 0 }}
      >
        SafePath AI Community Feed
      </motion.h1>

      <motion.div
        className="max-w-2xl mx-auto bg-black/30 p-6 rounded-2xl shadow-[0_0_30px_rgba(0,255,255,0.4)] border border-cyan-600/30 backdrop-blur-lg"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
      >
        <div className="space-y-4 max-h-[60vh] overflow-y-auto scrollbar-hide">
          {messages.map((msg, index) => (
            <motion.div
              key={index}
              className="p-4 rounded-xl bg-gray-800/40 border border-cyan-700/20 hover:border-cyan-400/50 transition"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
            >
              <div className="flex justify-between items-center">
                <span className="font-semibold text-cyan-300">{msg.user}</span>
                <div className="flex gap-1">
                  {Array(msg.rating)
                    .fill()
                    .map((_, i) => (
                      <Star key={i} className="text-yellow-400 w-4 h-4 fill-yellow-400" />
                    ))}
                </div>
              </div>
              <p className="mt-2 text-gray-200">{msg.text}</p>
            </motion.div>
          ))}
        </div>

        <div className="flex mt-6 gap-3">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Share your safety tip or alert..."
            className="flex-1 px-4 py-3 rounded-xl bg-gray-900/70 border border-cyan-600/40 focus:border-cyan-400 outline-none text-white placeholder-gray-500"
          />
          <button
            onClick={sendMessage}
            className="p-3 rounded-xl bg-gradient-to-r from-cyan-500 to-purple-500 hover:from-purple-600 hover:to-cyan-500 transition shadow-[0_0_20px_rgba(0,255,255,0.4)]"
          >
            <Send className="w-5 h-5" />
          </button>
        </div>
      </motion.div>

      <motion.div
        className="text-center mt-10 text-cyan-400/70 text-sm flex items-center justify-center gap-2"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.5 }}
      >
        <MessageCircle className="w-4 h-4" /> Join the community — help others stay safe!
      </motion.div>
    </div>
  );
}
