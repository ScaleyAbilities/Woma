using System;
using System.IO;
using System.Linq;
using System.Threading.Tasks;

namespace Woma
{
    class Program
    {
        internal static int Instances = int.Parse(Environment.GetEnvironmentVariable("INSTANCES") ?? "1");

        static void Main(string[] args)
        {
            if (args.Length < 1) {
                Console.WriteLine("No file specified.");
                Environment.Exit(1);
            }

            var filename = args[0];
            if (!File.Exists(filename)) {
                Console.WriteLine("File doesn't exist.");
                Environment.Exit(1);
            }

            var lines = File.ReadLines(filename);

            Console.WriteLine("Inserting Records...");

            for (var i = 1; i <= Instances; i++)
            {
                var instance = i; // Fixes closure issues
                Task.Run(() => {
                    lines.Where(l => {
                        
                    })
                });
            }
        }
    }
}
